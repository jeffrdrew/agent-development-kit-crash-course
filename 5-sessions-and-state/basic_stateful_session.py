import asyncio
import json
import uuid
from datetime import datetime

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()


# Create a new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Coco Drew",
    "user_preferences": """
        I like to sleep, play edge of the bed, get pet.
        My favorite food is Port Salut.
        My favorite TV show is All Creatures Great and Small.
        Loves it when people pet her.
    """,
}


async def main():
    run_id = "run1"
    log_path = "/Users/jeffreydrew/Documents/GitHub/agent-development-kit-crash-course/.cursor/debug.log"
    
    # #region debug log
    with open(log_path, 'a') as f:
        f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "A", "location": "basic_stateful_session.py:32", "message": "Before create_session call", "data": {}}).strip() + "\n")
    # #endregion
    
    # Create a NEW session
    APP_NAME = "Coco Bot"
    USER_ID = "coco_drew"
    SESSION_ID = str(uuid.uuid4())
    
    # #region debug log
    with open(log_path, 'a') as f:
        f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "B", "location": "basic_stateful_session.py:39", "message": "Calling create_session", "data": {"has_await": True}}).strip() + "\n")
    # #endregion
    
    try:
        stateful_session =  await session_service_stateful.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state=initial_state,
        )
        # #region debug log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "B", "location": "basic_stateful_session.py:48", "message": "create_session completed", "data": {"session_type": str(type(stateful_session)), "has_state": hasattr(stateful_session, 'state')}}).strip() + "\n")
        # #endregion
    except Exception as e:
        # #region debug log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "B", "location": "basic_stateful_session.py:52", "message": "create_session exception", "data": {"error_type": str(type(e).__name__), "error_msg": str(e)}}).strip() + "\n")
        # #endregion
        raise

    print("CREATED NEW SESSION:")
    print(f"Session ID: {SESSION_ID}")
    
    # #region debug log
    with open(log_path, 'a') as f:
        f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "E", "location": "basic_stateful_session.py:68", "message": "Accessing stateful_session.state", "data": {"state_exists": hasattr(stateful_session, 'state'), "state_type": str(type(stateful_session.state)) if hasattr(stateful_session, 'state') else None}}).strip() + "\n")
    # #endregion
    
    for key, value in stateful_session.state.items():
        print(f"{key}: {value}")
    print("--------------------------------")

    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role="user", parts=[types.Part(text="What is Coco Drew's favorite TV show?")]
    )

    # #region debug log
    with open(log_path, 'a') as f:
        f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "C", "location": "basic_stateful_session.py:84", "message": "Before runner.run", "data": {}}).strip() + "\n")
    # #endregion
    
    try:
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(f"Final Response: {event.content.parts[0].text}")
        # #region debug log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "C", "location": "basic_stateful_session.py:96", "message": "runner.run completed", "data": {}}).strip() + "\n")
        # #endregion
    except Exception as e:
        # #region debug log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "C", "location": "basic_stateful_session.py:100", "message": "runner.run exception", "data": {"error_type": str(type(e).__name__), "error_msg": str(e)}}).strip() + "\n")
        # #endregion
        raise

    print("==== Session Event Exploration ====")
    
    # #region debug log
    with open(log_path, 'a') as f:
        get_session_method = getattr(session_service_stateful, 'get_session', None)
        f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "A", "location": "basic_stateful_session.py:106", "message": "Before get_session call", "data": {"has_await": False, "method_type": str(type(get_session_method)), "is_coroutine": str(type(get_session_method)) if get_session_method else None}}).strip() + "\n")
    # #endregion
    
    try:
        session = await session_service_stateful.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        # #region debug log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "A", "location": "basic_stateful_session.py:113", "message": "get_session completed", "data": {"session_type": str(type(session)), "is_none": session is None}}).strip() + "\n")
        # #endregion
    except Exception as e:
        # #region debug log
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": run_id, "hypothesisId": "A", "location": "basic_stateful_session.py:118", "message": "get_session exception", "data": {"error_type": str(type(e).__name__), "error_msg": str(e)}}).strip() + "\n")
        # #endregion
        raise

    print(f"session: {session}")
    print(f"session.state: {session.state}")
    print(f"session.state.items: {session.state.items()}")
    print(f"session.state.keys: {session.state.keys()}")
    print(f"session.state.values: {session.state.values()}")
    print(f"session.state.get('user_name'): {session.state.get('user_name')}")
    print(f"session.state.get('user_preferences'): {session.state.get('user_preferences')}")
    print(f"session.state.get('user_preferences'): {session.state.get('user_preferences')}")

    print("++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++")

    # Log final Session state
    print("=== Final Session State ===")
    for key, value in session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    log_path = "/Users/jeffreydrew/Documents/GitHub/agent-development-kit-crash-course/.cursor/debug.log"
    try:
        asyncio.run(main())
    except Exception as e:
        import json
        from datetime import datetime
        with open(log_path, 'a') as f:
            f.write(json.dumps({"timestamp": datetime.now().timestamp(), "sessionId": "debug-session", "runId": "run1", "hypothesisId": "ALL", "location": "basic_stateful_session.py:155", "message": "Top-level exception in asyncio.run", "data": {"error_type": str(type(e).__name__), "error_msg": str(e), "error_repr": repr(e)}}).strip() + "\n")
        raise
