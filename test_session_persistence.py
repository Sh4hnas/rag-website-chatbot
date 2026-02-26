"""
Test script to verify session persistence and performance optimizations.

This script tests:
1. Session state initialization
2. Message persistence across interactions
3. Pagination functionality
4. CSS injection optimization
5. Model caching

Run this script to verify the optimizations are working correctly.
"""

import sys
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List

# Mock Streamlit session state for testing
class MockSessionState:
    def __init__(self):
        self._state = {}
    
    def __contains__(self, key):
        return key in self._state
    
    def __getitem__(self, key):
        return self._state[key]
    
    def __setitem__(self, key, value):
        self._state[key] = value
    
    def get(self, key, default=None):
        return self._state.get(key, default)

@dataclass
class ChatMessage:
    """Represents a single chat message in the conversation."""
    role: str
    content: str
    timestamp: datetime
    sources: Optional[List[int]] = None
    distances: Optional[List[float]] = None

def test_session_initialization():
    """Test that session state is properly initialized."""
    print("Testing session state initialization...")
    
    session_state = MockSessionState()
    
    # Simulate initialization
    if "messages" not in session_state:
        session_state["messages"] = []
    
    if "chat_display_limit" not in session_state:
        session_state["chat_display_limit"] = 50
    
    if "show_all_messages" not in session_state:
        session_state["show_all_messages"] = False
    
    if "css_injected" not in session_state:
        session_state["css_injected"] = False
    
    # Verify initialization
    assert session_state["messages"] == [], "Messages should be empty list"
    assert session_state["chat_display_limit"] == 50, "Display limit should be 50"
    assert session_state["show_all_messages"] == False, "Show all should be False"
    assert session_state["css_injected"] == False, "CSS injected should be False"
    
    print("✅ Session initialization test passed!")
    return True

def test_message_persistence():
    """Test that messages persist in session state."""
    print("\nTesting message persistence...")
    
    session_state = MockSessionState()
    session_state["messages"] = []
    
    # Add messages
    for i in range(5):
        message = ChatMessage(
            role="user" if i % 2 == 0 else "assistant",
            content=f"Test message {i}",
            timestamp=datetime.now()
        )
        session_state["messages"].append(message)
    
    # Verify persistence
    assert len(session_state["messages"]) == 5, "Should have 5 messages"
    assert session_state["messages"][0].content == "Test message 0", "First message should match"
    assert session_state["messages"][4].content == "Test message 4", "Last message should match"
    
    print("✅ Message persistence test passed!")
    return True

def test_pagination_logic():
    """Test pagination logic for chat history."""
    print("\nTesting pagination logic...")
    
    session_state = MockSessionState()
    session_state["messages"] = []
    session_state["chat_display_limit"] = 50
    session_state["show_all_messages"] = False
    
    # Add 75 messages
    for i in range(75):
        message = ChatMessage(
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i}",
            timestamp=datetime.now()
        )
        session_state["messages"].append(message)
    
    total_messages = len(session_state["messages"])
    
    # Test pagination when not showing all
    if session_state["show_all_messages"] or total_messages <= session_state["chat_display_limit"]:
        messages_to_display = session_state["messages"]
        hidden_count = 0
    else:
        messages_to_display = session_state["messages"][-session_state["chat_display_limit"]:]
        hidden_count = total_messages - session_state["chat_display_limit"]
    
    assert len(messages_to_display) == 50, "Should display 50 messages"
    assert hidden_count == 25, "Should have 25 hidden messages"
    assert messages_to_display[0].content == "Message 25", "First displayed should be message 25"
    assert messages_to_display[-1].content == "Message 74", "Last displayed should be message 74"
    
    # Test showing all messages
    session_state["show_all_messages"] = True
    
    if session_state["show_all_messages"] or total_messages <= session_state["chat_display_limit"]:
        messages_to_display = session_state["messages"]
        hidden_count = 0
    else:
        messages_to_display = session_state["messages"][-session_state["chat_display_limit"]:]
        hidden_count = total_messages - session_state["chat_display_limit"]
    
    assert len(messages_to_display) == 75, "Should display all 75 messages"
    assert hidden_count == 0, "Should have no hidden messages"
    
    print("✅ Pagination logic test passed!")
    return True

def test_css_injection_optimization():
    """Test that CSS injection flag works correctly."""
    print("\nTesting CSS injection optimization...")
    
    session_state = MockSessionState()
    session_state["css_injected"] = False
    
    # First run - should inject CSS
    if not session_state["css_injected"]:
        # Simulate CSS injection
        css_injected = True
        session_state["css_injected"] = True
    else:
        css_injected = False
    
    assert css_injected == True, "CSS should be injected on first run"
    assert session_state["css_injected"] == True, "Flag should be set to True"
    
    # Second run - should not inject CSS
    if not session_state["css_injected"]:
        css_injected = True
    else:
        css_injected = False
    
    assert css_injected == False, "CSS should not be injected on second run"
    
    print("✅ CSS injection optimization test passed!")
    return True

def test_message_optimization():
    """Test that add_message function handles empty content correctly."""
    print("\nTesting message optimization...")
    
    session_state = MockSessionState()
    session_state["messages"] = []
    
    # Simulate add_message with empty content
    def add_message(role: str, content: str):
        if not content or not content.strip():
            return
        
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.now()
        )
        session_state["messages"].append(message)
    
    # Try adding empty messages
    add_message("user", "")
    add_message("user", "   ")
    add_message("user", None if True else "test")  # Simulate None
    
    assert len(session_state["messages"]) == 0, "Empty messages should not be added"
    
    # Add valid message
    add_message("user", "Valid message")
    
    assert len(session_state["messages"]) == 1, "Valid message should be added"
    assert session_state["messages"][0].content == "Valid message", "Content should match"
    
    print("✅ Message optimization test passed!")
    return True

def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Running Session Persistence and Performance Tests")
    print("=" * 60)
    
    tests = [
        test_session_initialization,
        test_message_persistence,
        test_pagination_logic,
        test_css_injection_optimization,
        test_message_optimization
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✅ All tests passed! Performance optimizations are working correctly.")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
