"""
测试 Chat Feedback API
"""

from fastapi.testclient import TestClient

from app.core.database import SessionLocal, init_db
from app.main import app
from app.models import ChatMessage, ChatSession

init_db()
client = TestClient(app)


def _setup_test_data():
    db = SessionLocal()
    try:
        existing = db.query(ChatSession).filter(ChatSession.knowledge_base_id == 999).first()
        if existing:
            return existing.id
        session = ChatSession(knowledge_base_id=999, title="测试会话")
        db.add(session)
        db.flush()
        msg = ChatMessage(session_id=session.id, role="assistant", content="test reply")
        db.add(msg)
        db.commit()
        return session.id, msg.id
    finally:
        db.close()


def _login():
    resp = client.post("/api/login", json={"username": "admin", "password": "123456"})
    return resp.json()["data"]["token"]


token = _login()
headers = {"Authorization": f"Bearer {token}"}

session_id, message_id = _setup_test_data()

# 不需要真正的 knowledge_base，用 999 进行测试
# 但 feedback 接口会检查 knowledge_base 是否存在，所以先创建一个
resp = client.post(
    "/api/knowledge-bases",
    json={"name": "test-feedback", "description": ""},
    headers=headers,
)
kb_id = resp.json()["data"]["id"]

# 创建一个真实的 session 和 message
db = SessionLocal()
try:
    session = ChatSession(knowledge_base_id=kb_id, title="测试反馈会话")
    db.add(session)
    db.flush()
    msg = ChatMessage(session_id=session.id, role="assistant", content="这是一条测试回复")
    db.add(msg)
    db.commit()
    real_session_id = session.id
    real_message_id = msg.id
finally:
    db.close()

# Test 1: 提交 thumbs_up 反馈
resp = client.post(
    f"/api/knowledge-bases/{kb_id}/chat/feedback",
    json={"session_id": real_session_id, "message_id": real_message_id, "feedback": "thumbs_up"},
    headers=headers,
)
assert resp.status_code == 200, f"Test 1 failed: {resp.status_code} {resp.text}"
data = resp.json()
assert data["code"] == 0, f"Test 1 failed: {data}"
assert data["data"]["feedback"] == "thumbs_up"
print("  [PASS] 提交 thumbs_up 反馈成功")

# Test 2: 更新为 thumbs_down
resp = client.post(
    f"/api/knowledge-bases/{kb_id}/chat/feedback",
    json={
        "session_id": real_session_id,
        "message_id": real_message_id,
        "feedback": "thumbs_down",
        "comment": "回答不准确",
    },
    headers=headers,
)
assert resp.status_code == 200
data = resp.json()
assert data["code"] == 0
assert data["data"]["feedback"] == "thumbs_down"
print("  [PASS] 更新反馈为 thumbs_down 成功")

# Test 3: 无效的 feedback 值
resp = client.post(
    f"/api/knowledge-bases/{kb_id}/chat/feedback",
    json={"session_id": real_session_id, "message_id": real_message_id, "feedback": "invalid"},
    headers=headers,
)
assert resp.status_code == 400
print("  [PASS] 无效 feedback 值正确拒绝")

# Test 4: 不存在的消息
resp = client.post(
    f"/api/knowledge-bases/{kb_id}/chat/feedback",
    json={"session_id": real_session_id, "message_id": 99999, "feedback": "thumbs_up"},
    headers=headers,
)
assert resp.status_code == 404
print("  [PASS] 不存在消息正确返回 404")

# Test 5: 不存在的 knowledge base
resp = client.post(
    "/api/knowledge-bases/99999/chat/feedback",
    json={"session_id": real_session_id, "message_id": real_message_id, "feedback": "thumbs_up"},
    headers=headers,
)
assert resp.status_code == 404
print("  [PASS] 不存在知识库正确返回 404")

print("\n所有测试通过!")
