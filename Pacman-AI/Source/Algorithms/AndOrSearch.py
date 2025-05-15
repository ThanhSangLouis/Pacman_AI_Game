from Utils.utils import DDX, isValid2
from constants import FOOD

ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

def apply_action(state, action, _map, N, M):
    row, col = state
    if action == 'UP':
        target = (row - 1, col)
    elif action == 'DOWN':
        target = (row + 1, col)
    elif action == 'LEFT':
        target = (row, col - 1)
    elif action == 'RIGHT':
        target = (row, col + 1)
    else:
        return [state]

    # Kiểm tra xem di chuyển có hợp lệ không
    if isValid2(_map, target[0], target[1], N, M):
        return [target]  # Nếu hợp lệ, trả về vị trí mới
    return [state]  # Nếu không hợp lệ, trả về trạng thái hiện tại

def is_goal(food_pos, row, col):
    return (row, col) in food_pos

def and_or_graph_search(_map, state, N, M, goal_set):
    def andorsearch(state, path):
        print("🟡 OR node:", state)

        if is_goal(goal_set, state[0], state[1]):
            print("🎯 REACHED GOAL at", state)
            return 'GOAL'

        if state in path:
            print("🔁 LOOP DETECTED at", state)
            return 'FAILURE'

        path = path + [state]  # Tạo bản sao, không sửa trực tiếp

        for action in ACTIONS:
            outcomes = apply_action(state, action, _map, N, M)
            subplans = []

            for outcome in outcomes:
                if outcome != state:  # Chỉ tiếp tục nếu trạng thái mới khác trạng thái hiện tại
                    subplan = andorsearch(outcome, path)
                    if subplan == 'FAILURE':
                        break
                    subplans.append(subplan)

            if len(subplans) == len(outcomes):
                return (action, subplans)

        return 'FAILURE'

    return andorsearch(state, [])

def extract_next_action(plan):
    if isinstance(plan, tuple):
        action, subplans = plan
        if isinstance(subplans, list) and len(subplans) > 0:
            return action, subplans[0]  # Trả về hành động hiện tại + kế hoạch tiếp theo
        else:
            return action, None
    return None, None

def get_first_action(plan):
    if not plan or plan == 'FAILURE':
        return None
    if isinstance(plan, tuple):
        return plan[0]
    return None

def move_from_action(state, action):
    row, col = state
    if action == 'UP': return (row - 1, col)
    if action == 'DOWN': return (row + 1, col)
    if action == 'LEFT': return (row, col - 1)
    if action == 'RIGHT': return (row, col + 1)
    return state