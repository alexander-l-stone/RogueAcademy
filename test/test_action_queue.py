from source.action.action_queue import ActionQueue
from source.action.action import Action

def test_can_instantiate_action():
    """
    Tests that Action imports properly and its constructor works.
    """
    assert Action
    action = Action('test', 1)
    assert type(action) is Action

def test_can_instantiate_action_queue():
    """
    Tests that Action Queue imports properly and its constructor works.
    """
    assert ActionQueue
    action_queue = ActionQueue()
    assert type(action_queue) is ActionQueue

def test_can_pop_empty_queue_for_no_effect():
    """
    Tests that popping an empty queue does nothing
    """
    action_queue = ActionQueue()
    action_queue.pop()
    assert len(action_queue.queue) == 0

def test_can_add_actions(action):
    """
    Tests that actions can be added to the queue
    """
    action_queue = ActionQueue()
    action_queue.append(action)
    assert action in action_queue.queue

def test_can_pop_actions(action):
    """
    Tests that after an action with time 1 is added to the queue, pop will remove it
    """
    action_queue = ActionQueue()
    action_queue.append(action)
    action_queue.pop()
    assert action not in action_queue.queue

def test_long_actions_remain_after_pop(long_action):
    """
    Tests that actions with sufficient time remaining are not popped after one pop
    Tests that their time remaining is adjusted.
    """
    action_queue = ActionQueue()
    action_queue.append(long_action)
    action_queue.pop()
    assert long_action in action_queue.queue
    assert long_action.time_remaining == 1

def test_long_actions_can_be_removed(long_action):
    """
    Tests that multiple pops will remove the action.
    """
    action_queue = ActionQueue()
    action_queue.append(long_action)
    action_queue.pop()
    action_queue.pop()
    assert long_action not in action_queue.queue

def test_multiple_actions_resolve_at_once(action):
    """
    This tests to see if multiple actions can get removed at once
    """
    action_queue = ActionQueue()
    action_queue.append(action)
    second_action = Action('self', 1)
    action_queue.append(second_action)
    action_queue.pop()
    assert action not in action_queue.queue 
    assert second_action not in action_queue.queue

def test_actions_of_different_times_handled_properly(action, long_action):
    """
    This tests to see if this can handle actions of different times
    """
    second_action = Action('self', 1)
    action_queue = ActionQueue()
    action_queue.append(second_action)
    action_queue.append(long_action)
    action_queue.pop()
    assert long_action in action_queue.queue
    assert long_action.time_remaining == 1
    assert second_action not in action_queue.queue

#TODO: Write tests for player count
