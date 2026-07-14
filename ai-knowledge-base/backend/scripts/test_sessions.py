from fastapi.testclient import TestClient

from app.main import app


def _get_token(client: TestClient) -> str:
    response = client.post(
        "/api/login",
        json={"username": "admin", "password": "123456"},
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    return data["token"]


def test_chat_session_persistence():
    with TestClient(app) as client:
        token = _get_token(client)
        headers = {"Authorization": f"Bearer {token}"}

        save_payload = {
            "messages": [
                {"role": "user", "content": "什么是 RAG？"},
                {"role": "assistant", "content": "RAG 是检索增强生成。"},
            ]
        }
        save_response = client.post(
            "/api/knowledge-bases/1/chat/sessions",
            json=save_payload,
            headers=headers,
        )
        assert save_response.status_code == 200, save_response.text

        save_body = save_response.json()
        assert save_body["code"] == 0
        assert save_body["data"]["title"] == "什么是 RAG？"
        assert len(save_body["data"]["messages"]) == 2

        list_response = client.get(
            "/api/knowledge-bases/1/chat/sessions",
            headers=headers,
        )
        assert list_response.status_code == 200, list_response.text

        list_body = list_response.json()
        assert list_body["code"] == 0
        assert len(list_body["data"]["items"]) >= 1
        assert list_body["data"]["active_session"]["id"] == save_body["data"]["id"]
        assert len(list_body["data"]["active_session"]["messages"]) == 2


if __name__ == "__main__":
    test_chat_session_persistence()
    print("\nDay 6 session tests passed!")
