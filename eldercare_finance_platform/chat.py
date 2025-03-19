from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
import openai
import os
import json
import threading
from datetime import datetime

from . import db
from .models import ChatHistory, ChatSession

bp = Blueprint('chat', __name__, url_prefix='/chat')

# 存储生成任务的字典
generating_tasks = {}

@bp.route('/', methods=['GET'])
@login_required
def chat_interface():
    return render_template('chat/chat.html')

@bp.route('/new', methods=['GET'])
@login_required
def new_chat():
    # 创建新的聊天会话
    new_session = ChatSession(
        user_id=current_user.id,
        title="新对话",
        created_at=datetime.now()
    )
    db.session.add(new_session)
    db.session.commit()
    
    # 清除当前会话中的聊天历史
    session['chat_history'] = []
    session['current_chat_id'] = new_session.id
    
    return redirect(url_for('chat.chat_interface'))

@bp.route('/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    user_message = data.get('message', '')
    file_content = data.get('file_content', None)
    file_name = data.get('file_name', None)
    
    # 如果有文件内容，添加到用户消息中
    if file_content and file_name:
        user_message += f"\n\n附件 ({file_name}):\n```\n{file_content}\n```"
    
    # 获取会话中的聊天历史，如果没有则创建新的
    chat_history = session.get('chat_history', [])
    
    # 添加用户消息到历史记录
    chat_history.append({"role": "user", "content": user_message})
    
    # 生成任务ID
    task_id = f"task_{current_user.id}_{datetime.now().timestamp()}"
    generating_tasks[task_id] = {"status": "running", "stop_requested": False}
    
    # 调用OpenAI API
    try:
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        openai.api_base = os.environ.get('OPENAI_API_BASE')
        
        # 使用OpenAI客户端
        client = openai.OpenAI(
            api_key=openai.api_key,
            base_url=openai.api_base
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的养老金融顾问，擅长为老年人提供金融咨询、理财建议和风险管理方案。请用简单易懂的语言回答问题，避免使用过于专业的术语。支持Markdown格式和LaTeX公式。"},
                *chat_history
            ]
        )
        
        # 获取AI回复
        ai_message = response.choices[0].message.content
        
        # 添加AI回复到历史记录
        chat_history.append({"role": "assistant", "content": ai_message})
        
        # 更新会话中的聊天历史
        session['chat_history'] = chat_history
        
        # 获取当前聊天会话ID，如果没有则创建新的
        chat_session_id = session.get('current_chat_id')
        if not chat_session_id:
            new_session = ChatSession(
                user_id=current_user.id,
                title=user_message[:30] + "..." if len(user_message) > 30 else user_message,
                created_at=datetime.now()
            )
            db.session.add(new_session)
            db.session.commit()
            chat_session_id = new_session.id
            session['current_chat_id'] = chat_session_id
        
        # 保存聊天记录到数据库
        new_history = ChatHistory(
            user_id=current_user.id,
            session_id=chat_session_id,
            message=user_message,
            response=ai_message,
            timestamp=datetime.now()
        )
        db.session.add(new_history)
        db.session.commit()
        
        # 更新任务状态
        generating_tasks[task_id]["status"] = "completed"
        
        return jsonify({
            "success": True,
            "message": ai_message,
            "task_id": task_id
        })
    
    except Exception as e:
        # 更新任务状态
        generating_tasks[task_id]["status"] = "failed"
        
        return jsonify({
            "success": False,
            "error": str(e),
            "task_id": task_id
        }), 500

@bp.route('/stop_generating', methods=['POST'])
@login_required
def stop_generating():
    data = request.get_json()
    task_id = data.get('task_id')
    
    if task_id and task_id in generating_tasks:
        generating_tasks[task_id]["stop_requested"] = True
        return jsonify({
            "success": True,
            "message": "生成已停止"
        })
    
    return jsonify({
        "success": False,
        "message": "未找到生成任务"
    }), 404

@bp.route('/get_history', methods=['GET'])
@login_required
def get_history():
    # 获取用户的所有聊天会话
    sessions = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.created_at.desc()).all()
    
    # 格式化会话列表
    formatted_sessions = []
    for session in sessions:
        # 获取会话的第一条消息作为标题
        first_message = ChatHistory.query.filter_by(session_id=session.id).order_by(ChatHistory.timestamp.asc()).first()
        
        formatted_sessions.append({
            "id": session.id,
            "title": session.title if session.title else "新对话",
            "first_message": first_message.message if first_message else "",
            "created_at": session.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({
        "success": True,
        "sessions": formatted_sessions
    })

@bp.route('/get_session/<int:session_id>', methods=['GET'])
@login_required
def get_session(session_id):
    # 验证会话所有权
    session_obj = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
    if not session_obj:
        return jsonify({
            "success": False,
            "message": "未找到聊天会话"
        }), 404
    
    # 获取会话的所有消息
    messages = ChatHistory.query.filter_by(session_id=session_id).order_by(ChatHistory.timestamp.asc()).all()
    
    # 格式化消息
    formatted_messages = []
    chat_history = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "user_message": msg.message,
            "ai_response": msg.response,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
        
        chat_history.append({"role": "user", "content": msg.message})
        chat_history.append({"role": "assistant", "content": msg.response})
    
    # 更新会话中的聊天历史和当前会话ID
    session['chat_history'] = chat_history
    session['current_chat_id'] = session_id
    
    return jsonify({
        "success": True,
        "session": {
            "id": session_obj.id,
            "title": session_obj.title,
            "created_at": session_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        },
        "messages": formatted_messages
    })

@bp.route('/clear', methods=['POST'])
@login_required
def clear_history():
    # 清除会话中的聊天历史
    session['chat_history'] = []
    
    # 获取当前会话ID
    current_chat_id = session.get('current_chat_id')
    if current_chat_id:
        # 删除数据库中的聊天记录
        ChatHistory.query.filter_by(session_id=current_chat_id).delete()
        db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "聊天历史已清除"
    })

@bp.route('/delete_session/<int:session_id>', methods=['POST'])
@login_required
def delete_session(session_id):
    # 验证会话所有权
    session_obj = ChatSession.query.filter_by(id=session_id, user_id=current_user.id).first()
    if not session_obj:
        return jsonify({
            "success": False,
            "message": "未找到聊天会话"
        }), 404
    
    # 删除会话及其所有消息
    ChatHistory.query.filter_by(session_id=session_id).delete()
    db.session.delete(session_obj)
    db.session.commit()
    
    # 如果删除的是当前会话，清除会话中的聊天历史
    if session.get('current_chat_id') == session_id:
        session['chat_history'] = []
        session.pop('current_chat_id', None)
    
    return jsonify({
        "success": True,
        "message": "聊天会话已删除"
    })
