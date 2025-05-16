# 🟡 Pacman-AI Game
![Home](ImageREADME/Home.png)

## 🎯 GIỚI THIỆU TỔNG QUAN

Dự án **Pacman-AI** là một sản phẩm học thuật được thực hiện bởi nhóm 13 trong khuôn khổ môn học **Trí tuệ Nhân tạo** tại Trường Đại học Sư phạm Kỹ thuật TP.HCM. Dự án kế thừa gameplay cổ điển của trò chơi Pacman nhưng thay vì người chơi trực tiếp điều khiển, nhân vật Pacman sẽ được dẫn dắt **tự động hoàn toàn bằng các thuật toán AI** theo từng cấp độ và môi trường khác nhau.

![Home](ImageREADME/Game1.png)

> Không chỉ là một trò chơi giải trí, dự án là một sân chơi học thuật sáng tạo, giúp sinh viên vận dụng lý thuyết vào thực tiễn, trực quan hóa quá trình tìm kiếm và ra quyết định của các thuật toán.

## 🧠 MỤC TIÊU DỰ ÁN

* Triển khai **14 thuật toán AI** theo 7 nhóm lớn để điều khiển Pacman và Ghost.
* Cho phép người dùng tùy chọn **thuật toán** và **bản đồ** để trải nghiệm và đánh giá trực quan.
* Phân chia **4 cấp độ độ khó**, mỗi cấp độ có các đặc trưng AI và độ thử thách riêng.
* So sánh hiệu quả giữa các thuật toán thông qua hành vi của Pacman: tối ưu, nhanh, cẩn thận hay liều lĩnh.
* Hỗ trợ sinh viên học tập, giảng viên trình bày minh họa bài giảng và làm nền tảng cho các nghiên cứu mở rộng.

## 🧩 MÔ HÌNH HOẠT ĐỘNG

Người dùng khởi chạy chương trình → Chọn **Level**, **Thuật toán**, **Bản đồ (.txt)** trong giao diện menu → Quan sát Pacman **tự động chơi** dựa trên thuật toán đã chọn → Kết thúc khi **ăn hết thức ăn** hoặc **bị bắt**.

![Home](ImageREADME/Game2.png)

## 🎮 PHÂN CẤP ĐỘ CHƠI (LEVEL)

| Level | Mô tả gameplay               | Môi trường             | AI Pacman                                                                                                  | AI Ghost             |
|-------|------------------------------|------------------------|------------------------------------------------------------------------------------------------------------|----------------------|
| 1     | Ăn 1 food, không có ghost    | Mê cung tĩnh           | UCS, DFS, BFS, Beam Search, Greedy, Backtracking + Forward Checking, Backtracking + AC3, AndOr, Q-Learning | Không có             |
| 2     | Ăn 1 food, có ghost đứng yên | Ghost thụ động         | BFS, DFS, UCS, Greedy, Beam Search, A*                                                                     | Đứng yên             |
| 3     | Nhiều food, ghost đi quanh   | Ghost tuần tra khu vực | SA Hill Climbing, Simulated Annealing                                                                      | Random theo vùng     |
| 4     | Ghost truy sát thông minh    | Môi trường bất định    | Simulated Annealing, Minimax, Alpha-Beta                                                                   | A* truy đuổi         |

> Các cấp độ được thiết kế tăng dần độ phức tạp, từ dễ dàng (level 1) đến môi trường đối kháng và không chắc chắn (level 4).

## 🧠 CÁC NHÓM THUẬT TOÁN TRIỂN KHAI

### 🔹 Nhóm 1: Tìm kiếm không có thông tin (Uninformed Search)

* **BFS (Breadth-First Search)**
* **DFS (Depth-First Search)**
* **UCS (Uniform Cost Search)**

➡️ Duyệt tuần tự, không cần biết trước đích. Chạy tốt trong môi trường đơn giản như level 1,2.

### 🔹 Nhóm 2: Tìm kiếm có thông tin (Informed Search)

* **A***: `f(n) = g(n) + h(n)`
* **Greedy Search**: chỉ xét `h(n)`
* **Beam Search**: tìm k đường tốt nhất hiện tại

➡️ Chạy nhanh hơn, định hướng đến đích tốt, thích hợp level 2 và ghost level 4.

### 🔹 Nhóm 3: Tìm kiếm cục bộ (Local Search)

* **Steepest-Ascent Hill Climbing**
* **Simulated Annealing**

➡️ Không cần nhớ toàn bộ không gian trạng thái. Có thể mắc kẹt (HC) hoặc vượt qua bẫy local optima (SA).

### 🔹 Nhóm 4: Tìm kiếm trong môi trường phức tạp

* **AND-OR Graph Search**

➡️ Trạng thái sau hành động không chắc chắn, giải bài toán cây AND-OR theo lý thuyết sách giáo khoa.

### 🔹 Nhóm 5: Học tăng cường (Reinforcement Learning)

* **Q-Learning**: chọn hành động tối ưu dựa vào ma trận Q-table đã huấn luyện trước

➡️ Pacman học cách chơi bằng thử-sai, ghi nhớ phần thưởng.

### 🔹 Nhóm 6: Tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Search)

* **Backtracking**
* **AC-3 (Arc Consistency 3)**

➡️ Áp dụng cho các bài toán có ràng buộc cứng như: không được đi vào tường, tránh ghost, giới hạn hướng đi,... Sử dụng kỹ thuật loại trừ miền giá trị không hợp lệ và quay lui để tìm lời giải thỏa mãn toàn bộ ràng buộc.

### 🔹 Nhóm 7: Tìm kiếm đối kháng (Adversarial Search)

* **Minimax**
* **Alpha-Beta Pruning**

➡️ Mô phỏng game 2 người. Pacman là Max, Ghost là Min. Sử dụng evaluation function có trọng số để đánh giá.

## 🎬 Minh họa các thuật toán theo 4 cấp độ (Level) và nhóm thuật toán

Tại mỗi cấp độ, các thuật toán được chạy thử thuộc một hoặc nhiều nhóm thuật toán trong tổng số 7 nhóm chính, giúp người dùng dễ quan sát và so sánh hiệu quả từng nhóm trong môi trường cụ thể.



### Level 1 — Mê cung tĩnh, không có ghost

- **Nhóm 1: Tìm kiếm không có thông tin (Uninformed Search)**
  - Uniform Cost Search (UCS)
    
  ![ucsfix2](https://github.com/user-attachments/assets/2fe84ff9-1f15-4c0d-87e3-83ee4d1a73cb)

  - Depth-First Search (DFS)

  ![dfsfix (1)](https://github.com/user-attachments/assets/4f7d3b0d-b9d7-419c-adfb-78a74f167bd4)

  - Breadth-First Search (BFS)  
  ![bfs (1)](https://github.com/user-attachments/assets/da72d783-d6f3-49ff-80f6-ac15aaa1d247)


- **Nhóm 2: Tìm kiếm có thông tin (Informed Search)**
  - Beam Search
    
  ![beamfix](https://github.com/user-attachments/assets/3ab92406-af03-47aa-a513-0ba510bd4cc1)

  - Greedy Search
    
  ![greedyfix (1)](https://github.com/user-attachments/assets/2e8ca6d9-4e3a-4a80-88f0-1d9900ecc255)


- **Nhóm 6: Tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Search)**
  - Backtracking + Forward Checking
    
  ![back1fix](https://github.com/user-attachments/assets/e8a8e5af-17a7-4fde-955d-8eb2b9da34d8)

  - Backtracking + AC-3
    
  ![back2-fixmp4](https://github.com/user-attachments/assets/d50ac9a3-e4da-4e19-91e3-03657526ecbb)

- **Nhóm 4: Tìm kiếm trong môi trường phức tạp**
  - AND-OR Graph Search
    
  ![andorfix](https://github.com/user-attachments/assets/44343f9b-fc4a-4b57-a96e-09d7e0ac4f19)

- **Nhóm 5: Học tăng cường (Reinforcement Learning)**
  - Q-Learning

  ![qlearningfix](https://github.com/user-attachments/assets/1cd7c91c-d5a4-43e5-8c96-e62ecafa584b)

### Level 2 — Có ghost đứng yên

- **Nhóm 1: Tìm kiếm không có thông tin**
  - BFS
    
  ![bfs2](https://github.com/user-attachments/assets/2e5e4c1e-90c9-4237-b5be-82acbee39b7d)

  - DFS
    
  ![dfs2](https://github.com/user-attachments/assets/2fc5eca4-b86c-4295-80bb-f3ee409d3e1e)

  - UCS
    
  ![ucs2 (1)](https://github.com/user-attachments/assets/5c3c71a8-afc8-4abd-b8d1-5a375112bdc2)

- **Nhóm 2: Tìm kiếm có thông tin**
  - Greedy Search
    
  ![greedy2](https://github.com/user-attachments/assets/8e7b36af-b792-4299-9649-14654a1a21d1)

  - Beam Search
     
  ![beam2](https://github.com/user-attachments/assets/ac72de3c-c69b-45b9-99d5-7da8f1f1a749)

  - A* Search
    
  ![a2](https://github.com/user-attachments/assets/64e95856-4c30-49e6-9080-0a665c545225)


### Level 3 — Ghost tuần tra khu vực

- **Nhóm 3: Tìm kiếm cục bộ (Local Search)**
  - Steepest-Ascent Hill Climbing
    
  ![hill3fixmp4](https://github.com/user-attachments/assets/6d8b7ccc-cf0c-4392-aa08-8d9e963e6014)


  - Simulated Annealing  

  ![si3](https://github.com/user-attachments/assets/21a34925-fbde-4cfa-9d86-b4070ab8fa8a)


### Level 4 — Ghost truy sát thông minh

- **Nhóm 7: Tìm kiếm đối kháng (Adversarial Search)**
  
  - Minimax
    
    ![minifinal](https://github.com/user-attachments/assets/fe541790-fd66-42d1-9926-09fd9dde18a0)

  
  - Alpha-Beta Pruning
    
    ![alphafinal](https://github.com/user-attachments/assets/d4705099-06f8-4821-900d-efd644f82f43)


## ⚖️ So sánh điểm số thực tế theo từng cấp độ (Level)

Ta thực hiện chạy thử đồng loạt các thuật toán trong từng level trên cùng một bản đồ mẫu tương ứng và ghi nhận điểm số trung bình Pacman đạt được. Kết quả giúp đánh giá hiệu quả từng nhóm thuật toán trong môi trường đặc thù của mỗi cấp độ.



### Level 1 — Mê cung tĩnh, không có ghost

Hình ảnh dưới đây minh họa kết quả chạy thực tế của các thuật toán tìm đường tại Level 1 trên cùng 1 bản đồ — một bản đồ mê cung tĩnh, không có ghost và chi phí di chuyển giữa các ô là như nhau. Đây là môi trường đơn giản nhưng là cơ sở để đánh giá khả năng tìm đường tối ưu (về bước đi và chi phí) của từng thuật toán trong điều kiện cơ bản nhất.

![Home](ImageREADME/Kq_lv1.png)

| Thuật toán               | 🎯 Điểm trung bình | 👣 Bước đi | 🔍 Node mở rộng | 📌 Đặc điểm chính                                                                 |
|--------------------------|--------------------|------------|------------------|----------------------------------------------------------------------------------|
| **BFS**                  | -66                | 87         | 269              | Tìm đường ngắn nếu chi phí đều, ổn định, chi phí mỗi ô đều như nhau nên tương đối giống UCS ở level này |
| **DFS**                  | -86                | 107        | 170              | Đi sâu dễ lạc hướng, không tối ưu, mở ít node                                    |
| **UCS**                  | -66                | 87         | 269              | Tối ưu chi phí, nhưng trong map đồng đều thì giống hệt BFS                      |
| **Beam Search**          | -66                | 87         | 252              | Giữ k hướng tốt nhất, nhanh hơn BFS nhưng có thể bỏ qua hướng tối ưu            |
| **Greedy Search**        | -86                | 89         | 151              | Ưu tiên gần đích, nhanh nhưng dễ đi sai nếu map phức tạp                         |
| **Backtracking + AC-3**  | -85                | 106        | 392              | Giải ràng buộc tốt, xử lý logic rõ ràng nhưng tốc độ hơi chậm so với các thuật toán khác   |
| **AND-OR Graph Search**  | -96                | 116        | 1210             |  Xây dựng cây kế hoạch bao phủ tất cả trường hợp, phù hợp môi trường không xác định, nhưng **cực kỳ tốn tài nguyên** do mở rộng rất nhiều node        |
| **Q-Learning**           | -96                | 104        | 107              | Học từ kinh nghiệm, hiệu quả khi đã huấn luyện đủ, ban đầu chạy thì chưa tối ưu nhưng nếu huấn luyện càng nhiều thì sẽ rất tối ưu    |

### 🔎 Nhận xét & Kết luận

- ✅ Trong môi trường chi phí đều và không có ghost, **BFS, UCS và Beam Search** đều cho đường đi ngắn với độ mở rộng tương đối nhiều nhưng hợp lý.
- 🔴 **DFS** và **Greedy** cho kết quả kém hơn về điểm, do định hướng cục bộ và dễ lạc hướng.
- 🔵 **Backtracking + AC-3** và **AND-OR Search** tuy xử lý được bài toán logic sâu hơn, nhưng **không cần thiết** cho bản đồ tĩnh → chi phí xử lý cao hơn nhiều.
- 🟡 **Q-Learning** chưa có lợi thế trong môi trường đơn giản, do chưa khai thác được khả năng học từ tương tác lâu dài -> tức là huấn luyện chưa đủ.

---

### Level 2 — Có ghost đứng yên

Hình ảnh dưới đây minh họa kết quả chạy thực tế của các thuật toán tìm đường tại Level 2 trên cùng 1 bản đồ — một bản đồ có ghost cố định, với độ khó vừa phải. Mỗi thuật toán được đánh giá dựa trên số bước đi (`steps`) và số node đã mở rộng (`expansions`). Đây là cơ sở để phân tích hiệu suất, mức độ tối ưu và khả năng tiết kiệm tài nguyên của từng thuật toán.

![Home](ImageREADME/Kq_lv2.png)

| Thuật toán       | 🎯 Điểm trung bình | 👣 Bước đi | 🔍 Node mở rộng | 📌 Đặc điểm chính                                                                 |
|------------------|--------------------|------------|------------------|----------------------------------------------------------------------------------|
| **BFS**          | 0                  | 21         | 81               | Tìm đường ngắn nhất về bước đi, mở rộng toàn diện cả map             |
| **DFS**          | -4                 | 25         | 28               | Đi sâu nhanh, dễ lạc hướng, mở ít node nhưng không tối ưu                       |
| **UCS**          | 0                  | 21         | 76               | Tối ưu tổng chi phí, né ghost bằng cost, nhưng mở rộng nhiều hơn               |
| **Greedy**       | -4                 | 25         | 27               | Nhanh, mở rất ít node, nhưng dễ đi sai                         |
| **Beam Search**  | 0                  | 21         | 47               | Chọn lọc hướng tốt bằng heuristic, cân bằng giữa tốc độ và chất lượng          |
| **A\***          | 0                  | 21         | 49               | Dùng `g(n) + h(n)` để tìm đường tối ưu, né ghost hiệu quả, mở rộng hợp lý       |

### 🔎 Nhận xét & Kết luận

- 🟢 **A\*** và **Beam Search** là hai thuật toán hoạt động hiệu quả nhất tại Level 2 — vừa đảm bảo được độ tối ưu, vừa kiểm soát được số node mở rộng.
- 🔵 **UCS** tìm đường an toàn với ghost nhưng phải đánh đổi bằng số lượng node mở rộng nhiều hơn.
- 🟡 **BFS** tuy ổn định và tìm được đường đi tối ưu nhưng tốn tài nguyên.
- 🔴 **DFS** và **Greedy** mở rất ít node nhưng thường đi sai hướng, dẫn đến đường đi dài và không hiệu quả.
- ✅ Trong môi trường có ghost, **heuristic tốt** và **cân bằng giữa `g(n)` và `h(n)`** là yếu tố then chốt giúp thuật toán hiệu quả hơn.

> 🎯 Tùy thuộc vào mục tiêu (tối ưu hóa, tốc độ hay tiết kiệm bộ nhớ), người dùng có thể lựa chọn thuật toán phù hợp thay vì chỉ dựa vào kết quả đường đi.

---

### Level 3 — Ghost tuần tra khu vực

Tại Level 3, ghost di chuyển tuần tra trên bản đồ khiến môi trường trở nên **động và khó đoán**. Các thuật toán phải thích nghi linh hoạt để vừa **né ghost**, vừa **tối ưu điểm số**. Dưới đây là so sánh giữa hai chiến lược:

| Thuật toán                | 🎯 Điểm trung bình | 📌 Đặc điểm chính                                                  |
|---------------------------|--------------------|-------------------------------------------------------------------|
| **Simulated Annealing**   | **207**            | Có khả năng "liều" chọn bước tạm thời kém để **thoát local maxima**, **né ghost hiệu quả** |
| **SA Hill Climbing**      | **137**            | **Nhanh, chọn bước tốt nhất**, nhưng dễ **mắc kẹt** nếu không có hướng đi tốt hơn, phải random hướng bất kì để thoát kẹt |


### 🔎 Nhận xét & Kết luận

- **Simulated Annealing** đạt điểm số cao hơn rõ rệt, nhờ khả năng **thoát khỏi bẫy cục bộ (local optima)** và thích nghi tốt trong môi trường ghost di chuyển.
- **SA Hill Climbing** tuy đơn giản và nhanh, nhưng lại dễ di chuyển quanh tại những khu vực tưởng chừng tối ưu — đặc biệt khi không thể đi hướng nào tốt hơn thì nó thoát ra bằng cách random 1 hướng đi mới.
- ✅ Với độ phức tạp của Level 3, **Simulated Annealing tỏ ra đáng tin cậy hơn** nhờ khả năng **chấp nhận rủi ro có kiểm soát** và **khám phá không gian trạng thái rộng hơn**.

> 🧠 Trong môi trường AI game động ở level này, **Nhóm thuật toán tìm kiếm cục bộ đạt ưu thế vượt trội, các nhóm khác khi áp dụng vào rất khó thắng**.

---

### Level 4 — Ghost truy sát thông minh

Tại Level 4, ghost không còn di chuyển ngẫu nhiên hay tuần tra đơn thuần mà được lập trình **truy sát Pacman một cách chủ động và thông minh hơn**. Đây là môi trường mang tính đối kháng cao, yêu cầu thuật toán phải **phán đoán hành vi đối phương** và **lập kế hoạch nhiều bước**.

| Thuật toán              | 🎯 Điểm trung bình | 📌 Đặc điểm chính                                                        |
|-------------------------|--------------------|-------------------------------------------------------------------------|
| **Minimax**             | **5157**           | Mô hình hóa trò chơi hai người chơi (Pacman vs Ghost), **ra quyết định thận trọng**, luôn chọn hành động tối ưu nhất để **né ghost** |
| **Alpha-Beta Pruning**  | **5157**           | Phiên bản tối ưu của Minimax, **cắt bớt các nhánh không cần thiết**, giúp **tăng tốc độ** mà vẫn giữ nguyên chất lượng quyết định |

### 🔍 Nhận xét & Kết luận

- Cả **Minimax** và **Alpha-Beta Pruning** đều mang lại chiến thắng với **điểm số rất cao**, thể hiện khả năng thích ứng vượt trội trong môi trường ghost truy đuổi.
- **Alpha-Beta Pruning** đặc biệt hiệu quả khi tăng độ sâu tìm kiếm, vì nó **loại bỏ những lựa chọn không cần thiết**, từ đó **tiết kiệm thời gian** mà không ảnh hưởng đến kết quả cuối cùng.
- ✅ Trong môi trường có sự đối kháng rõ rệt như Level 4, **thuật toán chiến lược như Minimax và Alpha-Beta Pruning là lựa chọn tối ưu**, vì chúng không chỉ tìm đường mà còn **phản ứng theo hành vi của đối thủ**.

> 🧠 Đây là minh chứng rõ ràng rằng: khi trò chơi không còn là một môi trường tĩnh, **các chiến lược ra quyết định với tư duy đối kháng sẽ chiếm ưu thế vượt trội**.

---

## 🧠 HÀM ĐÁNH GIÁ & CHI PHÍ

* **A***: `f(n) = g(n) + h(n)` với `h(n)` là khoảng cách Manhattan đến food.
* **Minimax**:
```python
score = food_count * 100 - ghost_distance * 150
```
* **Hill Climbing**: f(n) = h(n) - số lần đã đi qua ô đó
* **Simulated Annealing**: chấp nhận giải tạm thời tệ hơn dựa vào nhiệt độ T.

## 🖼️ GIAO DIỆN PHẦN MỀM

* Giao diện được xây dựng bằng **Pygame**, có hỗ trợ ảnh nền, nút hover, hiển thị trạng thái Pacman.
* 3 màn hình chính:
  * **Menu**: chọn level, thuật toán, bản đồ
  * **Game**: Pacman di chuyển tự động
  * **Kết thúc**: Thắng/Thua, hiển thị điểm và chọn chơi lại

## 📂 CẤU TRÚC FILE CHÍNH

```
Pacman_AI_Game/
├── Algorithms/       # Các file: BFS.py, AStar.py, Minimax.py...
├── Object/           # Các class: Player, Food, Ghost, Wall...
├── Input/            # Thư mục chứa map chia theo Level
├── Utils/            # File utils.py với các hàm tính toán chung
├── main.py           # Hàm startGame, xử lý thuật toán theo Level
├── constants.py      # Quy định map màu, ký hiệu, thuật toán từng Level
```

## ▶️ HƯỚNG DẪN CHẠY

**Bước 1:** Mở command line và chạy lệnh:

```bash
git clone https://github.com/ThanhSangLouis/Pacman_AI_Game.git
```

**Bước 2:** Bật console **cùng cấp** với file `main.py` (trong thư mục **Source**).

**Bước 3:**

* Nếu đã cài đặt Python và Pygame, bạn có thể bỏ qua bước này.
* Nếu chưa:
  * Tải Python tại: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  * Cài đặt Pygame bằng lệnh:

```bash
pip install pygame
```

* Hoặc cài đặt đầy đủ các thư viện:

```bash
pip install -r requirements.txt
```

**Bước 4:** Chạy chương trình với lệnh:

```bash
python main.py
```

Hoặc nếu dùng Windows:

```bash
py main.py
```

**Lưu ý cho người dùng PyCharm:**

* Mở thư mục chứa cả **Source** và **Input**.
* Mở file `main.py` trong PyCharm và nhấn nút Run ▶️ hoặc tổ hợp phím `Shift + F10` để khởi chạy chương trình.

## 🚀 MỞ RỘNG & ỨNG DỤNG

* Có thể tích hợp thêm thuật toán: Genetic Algorithm, Deep Q-Learning, Policy Gradient ...
* Mở rộng giao diện thêm phần phân tích thống kê: số bước, thời gian, số node mở rộng
* Tạo mode "Học vs Học": Q-Learning Pacman đấu DQN Ghost


## ✍️ TÁC GIẢ

Dự án được thực hiện bởi nhóm sinh viên lớp AI:

- **Lê Văn Chiến Thắng**  
- **Võ Thanh Sang**  
- **Trịnh Nguyễn Hoàng Nguyên**

Trường Đại học Sư phạm Kỹ thuật TP.HCM  
Môn học: Trí tuệ Nhân tạo  
Giảng viên hướng dẫn: TS. Phan Thị Huyền Trang

## 🌐 LINK DỰ ÁN

[🔗 GitHub Repository](https://github.com/ThanhSangLouis/Pacman_AI_Game)

## 📚 TÀI LIỆU THAM KHẢO

[1] Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.

[2] UC Berkeley AI. (2025, May 13). *Project 2: Multi-Agent Pacman*. UC Berkeley Artificial Intelligence.  
https://ai.berkeley.edu/multiget.html

[3] nxhawk. (2020, September 19). *Pacman-AI*. GitHub.  
https://github.com/nxhawk/Pacman-AI
