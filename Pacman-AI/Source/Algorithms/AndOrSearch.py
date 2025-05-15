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
        print("🟡 OR node:", state)  # Đây là node OR: lựa chọn hành động từ trạng thái hiện tại

        if is_goal(goal_set, state[0], state[1]):
            print("🎯 REACHED GOAL at", state)
            return 'GOAL'

        if state in path:
            print("🔁 LOOP DETECTED at", state)
            return 'FAILURE'

        path = path + [state]  # Sao chép path, không sửa path gốc

        # Duyệt từng hành động có thể thực hiện từ state hiện tại (node OR)
        for action in ACTIONS:
            outcomes = apply_action(state, action, _map, N, M)
            subplans = []

            print(f"    ⚙️ AND node for action '{action}': outcomes = {outcomes}")  
            # Node AND thể hiện các kết quả khác nhau của 1 hành động phải đều thành công

            # Với mỗi kết quả có thể của hành động, gọi đệ quy
            for outcome in outcomes:
                if outcome != state:  # Nếu trạng thái mới khác trạng thái hiện tại
                    subplan = andorsearch(outcome, path)
                    if subplan == 'FAILURE':
                        print(f"    ❌ Outcome {outcome} của action '{action}' thất bại, bỏ qua action này")
                        break  # Nếu một outcome fail, bỏ luôn hành động này
                    subplans.append(subplan)

            # Nếu tất cả các outcomes đều thành công (đủ số), trả về kế hoạch
            if len(subplans) == len(outcomes):
                print(f"    ✅ Action '{action}' thành công với subplans: {subplans}")
                return (action, subplans)

        # Nếu không hành động nào thành công, trả về failure
        print(f"❌ OR node tại {state} không có hành động thành công")
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