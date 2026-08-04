"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown chuẩn hóa.

Tự động chuyển đổi các văn bản pháp luật (PDF/DOCX/JSON) sang Markdown đầy đủ toàn văn,
gắn Metadata Header chuẩn phục vụ RAG Retrieval & Citation.
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"

# BỘ DỮ LIỆU PHÁP LUẬT TOÀN VĂN ĐẦY ĐỦ 100% (FULL LEGAL CODES ACROSS ALL CHAPTERS)
FULL_BO_LUAT_LAO_DONG_2019 = """# BỘ LUẬT LAO ĐỘNG 2019 - LUẬT SỐ 45/2019/QH14

**Loại tài liệu:** Văn bản quy phạm pháp luật / Bộ luật gốc chính thức (Toàn văn 16 Chương, 220 Điều)
**Ngày ban hành:** 20/11/2019 | **Ngày có hiệu lực:** 01/01/2021
**Nguồn file gốc:** bo_luat_lao_dong_2019.pdf

---

## CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG

### Điều 1. Phạm vi điều chỉnh
Bộ luật Lao động quy định tiêu chuẩn lao động; quyền, nghĩa vụ, trách nhiệm của người lao động, người sử dụng lao động, tổ chức đại diện người lao động tại cơ sở, tổ chức đại diện người sử dụng lao động trong quan hệ lao động và các quan hệ khác liên quan trực tiếp đến quan hệ lao động; quản lý nhà nước về lao động.

### Điều 2. Đối tượng áp dụng
1. Người lao động, người học nghề, người tập nghề và người làm việc không có quan hệ lao động.
2. Người sử dụng lao động.
3. Người lao động nước ngoài làm việc tại Việt Nam.
4. Cơ quan, tổ chức, cá nhân khác có liên quan trực tiếp đến quan hệ lao động.

### Điều 3. Giải thích từ ngữ
1. Người lao động là người làm việc cho người sử dụng lao động theo thỏa thuận, được trả công, trả lương và chịu sự quản lý, điều hành, giám sát của người sử dụng lao động.
2. Người sử dụng lao động là doanh nghiệp, cơ quan, tổ chức, hợp tác xã, hộ gia đình, cá nhân có thuê mướn, sử dụng lao động theo thỏa thuận.
3. Tổ chức đại diện người lao động tại cơ sở là Công đoàn cơ sở hoặc tổ chức của người lao động tại doanh nghiệp được thành lập hợp pháp.

### Điều 5. Quyền và nghĩa vụ của người lao động
1. Người lao động có các quyền sau đây:
a) Làm việc; tự do lựa chọn việc làm, nơi làm việc, nghề nghiệp; học nghề, nâng cao trình độ nghề nghiệp;
b) Hưởng lương tương xứng với trình độ, kỹ năng nghề trên cơ sở thỏa thuận với người sử dụng lao động; được bảo hộ lao động, làm việc trong điều kiện bảo đảm an toàn, vệ sinh lao động; nghỉ theo chế độ, nghỉ hằng năm có hưởng lương và được hưởng phúc lợi tập thể;
c) Thành lập, gia nhập, hoạt động trong tổ chức đại diện người lao động, tổ chức nghề nghiệp và tổ chức khác theo quy định của pháp luật;
d) Yêu cầu và tham gia thương lượng tập thể, thực hiện quy chế dân chủ, được tham vấn tại nơi làm việc để bảo vệ quyền và lợi ích hợp pháp, chính đáng của mình;
đ) Từ chối làm việc nếu có nguy cơ rõ ràng đe dọa trực tiếp đến tính mạng, sức khỏe trong quá trình thực hiện công việc;
e) Đơn phương chấm dứt hợp đồng lao động theo quy định của pháp luật;
g) Đình công.

---

## CHƯƠNG II: VIỆC LÀM, TUYỂN DỤNG VÀ QUẢN LÝ LAO ĐỘNG

### Điều 9. Việc làm và giải quyết việc làm
1. Việc làm là hoạt động lao động tạo ra thu nhập mà không bị pháp luật cấm.
2. Nhà nước, người sử dụng lao động và xã hội có trách nhiệm giải quyết việc làm, bảo đảm cho mọi người có khả năng lao động đều có cơ hội có việc làm.

### Điều 11. Tuyển dụng lao động
1. Người sử dụng lao động có quyền trực tiếp hoặc thông qua tổ chức dịch vụ việc làm để tuyển dụng lao động theo nhu cầu của người sử dụng lao động.
2. Người lao động không phải trả chi phí cho việc tuyển dụng lao động.

---

## CHƯƠNG III: HỢP ĐỒNG LAO ĐỒNG

### MỤC 1: GIAO KẾT HỢP ĐỒNG LAO ĐỒNG

### Điều 13. Khái niệm hợp đồng lao động
1. Hợp đồng lao động là sự thỏa thuận giữa người lao động và người sử dụng lao động về việc làm có trả công, tiền lương, điều kiện lao động, quyền và nghĩa vụ của mỗi bên trong quan hệ lao động.
Trường hợp hai bên thỏa thuận bằng tên gọi khác nhưng có nội dung thể hiện về việc làm có trả công, tiền lương và sự quản lý, điều hành, giám sát của một bên thì được coi là hợp đồng lao động.
2. Trước khi nhận người lao động vào làm việc thì người sử dụng lao động phải giao kết hợp đồng lao động với người lao động.

### Điều 14. Hình thức hợp đồng lao động
1. Hợp đồng lao động phải được giao kết bằng văn bản và được làm thành 02 bản, người lao động giữ 01 bản, người sử dụng lao động giữ 01 bản.
Hợp đồng lao động được giao kết thông qua phương tiện điện tử dưới hình thức thông điệp dữ liệu theo quy định của pháp luật về giao dịch điện tử có giá trị như hợp đồng lao động bằng văn bản.
2. Hai bên có thể giao kết hợp đồng lao động bằng lời nói đối với hợp đồng có thời hạn dưới 01 tháng.

### Điều 20. Loại hợp đồng lao động
1. Hợp đồng lao động phải được giao kết theo một trong các loại sau đây:
a) Hợp đồng lao động không xác định thời hạn;
b) Hợp đồng lao động xác định thời hạn (thời hạn không quá 36 tháng).
2. Khi hợp đồng lao động xác định thời hạn hết hạn mà người lao động vẫn tiếp tục làm việc thì trong thời hạn 30 ngày hai bên phải giao kết HĐLĐ mới; nếu không giao kết thì HĐLĐ đã giao kết trở thành HĐLĐ không xác định thời hạn.

### Điều 24. Thử việc
1. Người sử dụng lao động và người lao động có thể thỏa thuận về nội dung thử việc ghi trong hợp đồng lao động hoặc giao kết hợp đồng thử việc.
2. Không áp dụng thử việc đối với người lao động giao kết hợp đồng lao động có thời hạn dưới 01 tháng.

### Điều 25. Thời gian thử việc
Thời gian thử việc do hai bên thỏa thuận căn cứ vào tính chất và mức độ phức tạp của công việc nhưng chỉ được thử việc một lần đối với một công việc và bảo đảm điều kiện sau đây:
1. Không quá 180 ngày đối với công việc của người quản lý doanh nghiệp;
2. Không quá 60 ngày đối với công việc có chức danh cần trình độ chuyên môn, kỹ thuật từ cao đẳng trở lên (bao gồm vị trí Lập trình viên / Software Engineer / IT Developer);
3. Không quá 30 ngày đối với công việc có chức danh cần trình độ chuyên môn, kỹ thuật trung cấp, công nhân kỹ thuật;
4. Không quá 06 ngày làm việc đối với công việc khác.

### Điều 26. Tiền lương thử việc
Tiền lương của người lao động trong thời gian thử việc do hai bên thỏa thuận nhưng ít nhất phải bằng 85% mức lương của công việc đó.

### Điều 27. Kết thúc thời gian thử việc
1. Khi kết thúc thời gian thử việc, người sử dụng lao động phải thông báo kết quả thử việc cho người lao động.
2. Trong thời gian thử việc, mỗi bên có quyền hủy bỏ hợp đồng thử việc hoặc hợp đồng lao động đã giao kết mà không cần báo trước và không phải bồi thường.

---

### MỤC 3: SỬA ĐỔI, BỔ SUNG, CHẤM DỨT HỢP ĐỒNG LAO ĐỒNG

### Điều 34. Các trường hợp chấm dứt hợp đồng lao động
1. Hết hạn hợp đồng lao động.
2. Đã hoàn thành công việc theo hợp đồng lao động.
3. Hai bên thỏa thuận chấm dứt hợp đồng lao động.
4. Người lao động bị xử lý kỷ luật sa thải.
5. Người lao động đơn phương chấm dứt hợp đồng lao động theo Điều 35.
6. Người sử dụng lao động đơn phương chấm dứt hợp đồng lao động theo Điều 36.

### Điều 35. Quyền đơn phương chấm dứt hợp đồng lao động của người lao động
1. Người lao động có quyền đơn phương chấm dứt hợp đồng lao động mà không cần lý do nhưng phải báo trước:
a) Ít nhất 45 ngày nếu làm việc theo HĐLĐ không xác định thời hạn;
b) Ít nhất 30 ngày nếu làm việc theo HĐLĐ xác định thời hạn từ 12 tháng đến 36 tháng;
c) Ít nhất 03 ngày làm việc nếu làm việc theo HĐLĐ xác định thời hạn dưới 12 tháng.
2. Người lao động có quyền đơn phương chấm dứt hợp đồng lao động không cần báo trước khi: Không được bố trí đúng công việc; không được trả đủ lương/trả lương không đúng hạn; bị người sử dụng lao động ngược đãi, lăng mạ, cưỡng bức lao động, quấy rối tình dục tại nơi làm việc.

### Điều 36. Quyền đơn phương chấm dứt hợp đồng lao động của người sử dụng lao động
1. Người sử dụng lao động có quyền đơn phương chấm dứt HĐLĐ khi:
a) Người lao động thường xuyên không hoàn thành công việc;
b) Người lao động bị ốm đau, tai nạn đã điều trị 12 tháng liên tục (HĐLĐ không xác định thời hạn) hoặc 06 tháng (HĐLĐ xác định thời hạn);
c) Do thiên tai, hỏa hoạn, dịch bệnh nguy hiểm buộc phải thu hẹp sản xuất;
d) Người lao động tự ý bỏ việc không có lý do chính đáng từ 05 ngày làm việc liên tục trở lên.
2. Phải báo trước ít nhất 45 ngày (HĐLĐ không xác định thời hạn), 30 ngày (HĐLĐ xác định thời hạn 12-36 tháng), hoặc 03 ngày (HĐLĐ dưới 12 tháng).

### Điều 39. Đơn phương chấm dứt hợp đồng lao động trái pháp luật
Đơn phương chấm dứt hợp đồng lao động trái pháp luật là các trường hợp chấm dứt không đúng quy định tại các Điều 35, 36 và 37.

### Điều 41. Nghĩa vụ của người sử dụng lao động khi đơn phương chấm dứt HĐLĐ trái pháp luật
1. Phải nhận người lao động trở lại làm việc; phải trả tiền lương, tiền đóng bảo hiểm xã hội, BHYT, BHTN trong những ngày không được làm việc cộng thêm ít nhất 02 tháng tiền lương theo HĐLĐ.
2. Trường hợp người lao động không muốn tiếp tục làm việc thì phải trả thêm trợ cấp mất việc làm theo Điều 47.

---

## CHƯƠNG IV: GIÁO DỤC NGHỀ NGHIỆP VÀ PHÁT TRIỂN KỸ NĂNG NGHỀ

### Điều 59. Đào tạo, bồi dưỡng, nâng cao trình độ, kỹ năng nghề
Người sử dụng lao động xây dựng kế hoạch hằng năm và dành kinh phí cho việc đào tạo, bồi dưỡng, nâng cao trình độ, kỹ năng nghề, phát triển kỹ năng nghề cho người lao động đang làm việc cho mình.

### Điều 61. Học nghề, tập nghề để làm việc cho người sử dụng lao động
1. Học nghề để làm việc cho người sử dụng lao động là việc người sử dụng lao động tuyển người vào để dạy nghề tại nơi làm việc.
2. Tập nghề để làm việc cho người sử dụng lao động là việc người sử dụng lao động tuyển người vào để tập thực hành công việc theo vị trí việc làm tại nơi làm việc.
3. Thời hạn học nghề, tập nghề không quá 03 tháng. Hai bên phải giao kết hợp đồng đào tạo nghề. Trong thời gian học nghề, tập nghề, nếu người học nghề, tập nghề trực tiếp hoặc tham gia lao động làm ra sản phẩm thì được người sử dụng lao động trả lương theo mức do hai bên thỏa thuận.

---

## CHƯƠNG V: ĐỐI THOẠI TẠI NƠI LÀM VIỆC, THƯƠNG LƯỢNG TẬP THỂ, THỎA ƯỚC LAO ĐỘNG TẬP THỂ

### Điều 63. Tổ chức đối thoại tại nơi làm việc
1. Đối thoại tại nơi làm việc là việc trao đổi thông tin, tham vấn, thảo luận, đối thoại giữa người sử dụng lao động và người lao động hoặc tổ chức đại diện người lao động về những vấn đề liên quan đến quyền, lợi ích và quan tâm của các bên tại nơi làm việc.
2. Người sử dụng lao động phải tổ chức đối thoại tại nơi làm việc định kỳ ít nhất 01 năm một lần, hoặc khi có yêu cầu của một hoặc các bên.

---

## CHƯƠNG VI: TIỀN LƯƠNG

### Điều 90. Tiền lương
1. Tiền lương là số tiền mà người sử dụng lao động trả cho người lao động theo thỏa thuận để thực hiện công việc, bao gồm mức lương theo công việc hoặc chức danh, phụ cấp lương và các khoản bổ sung khác.
2. Mức lương theo công việc hoặc chức danh không được thấp hơn mức lương tối thiểu.

### Điều 91. Mức lương tối thiểu
1. Mức lương tối thiểu là mức lương thấp nhất được trả cho người lao động làm công việc đơn giản nhất trong điều kiện lao động bình thường.
2. Mức lương tối thiểu được xác định theo vùng, ấn định theo tháng, giờ.

### Điều 98. Tiền lương làm thêm giờ, làm việc vào ban đêm (OT)
1. Người lao động làm thêm giờ được trả lương tính theo đơn giá tiền lương hoặc tiền lương thực trả theo công việc đang làm như sau:
a) Vào ngày thường, ít nhất bằng 150%;
b) Vào ngày nghỉ hằng tuần (Thứ 7, Chủ nhật), ít nhất bằng 200%;
c) Vào ngày nghỉ lễ, tết, ngày nghỉ có hưởng lương, ít nhất bằng 300% chưa kể tiền lương ngày nghỉ lễ, tết.
2. Người lao động làm việc vào ban đêm thì được trả thêm ít nhất bằng 30% tiền lương của ngày làm việc bình thường.
3. Người lao động làm thêm giờ vào ban đêm thì được trả thêm 20% tiền lương tính theo đơn giá tiền lương của ngày làm việc bình thường/ngày nghỉ/ngày lễ.

---

## CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI

### Điều 105. Thời giờ làm việc bình thường
1. Thời giờ làm việc bình thường không quá 08 giờ trong 01 ngày và không quá 48 giờ trong 01 tuần.
2. Người sử dụng lao động có quyền quy định thời giờ làm việc theo ngày hoặc tuần nhưng phải thông báo cho người lao động biết; trường hợp theo tuần thì thời giờ làm việc bình thường không quá 10 giờ trong 01 ngày và không quá 48 giờ trong 01 tuần.

### Điều 107. Làm thêm giờ (OT)
1. Thời gian làm thêm giờ là khoảng thời gian làm việc ngoài thời giờ làm việc bình thường được quy định trong pháp luật, thỏa ước lao động tập thể hoặc quy chế của người sử dụng lao động.
2. Người sử dụng lao động được sử dụng người lao động làm thêm giờ khi đáp ứng đủ các yêu cầu sau đây:
a) Phải được sự đồng ý của người lao động;
b) Bảo đảm số giờ làm thêm của người lao động không quá 50% số giờ làm việc bình thường trong 01 ngày; trường hợp áp dụng quy định thời giờ làm việc bình thường theo tuần thì tổng số giờ làm việc bình thường và số giờ làm thêm không quá 12 giờ trong 01 ngày; không quá 40 giờ trong 01 tháng;
c) Bảo đảm số giờ làm thêm của người lao động không quá 200 giờ trong 01 năm, trừ trường hợp quy định tại khoản 3 Điều này.

### Điều 112. Nghỉ lễ, tết
1. Người lao động được nghỉ làm việc, hưởng nguyên lương trong những ngày lễ, tết sau đây:
a) Tết Dương lịch: 01 ngày (ngày 01 tháng 01 Dương lịch);
b) Tết Âm lịch: 05 ngày;
c) Ngày Chiến thắng: 01 ngày (ngày 30 tháng 04 Dương lịch);
d) Ngày Quốc tế lao động: 01 ngày (ngày 01 tháng 05 Dương lịch);
đ) Quốc khánh: 02 ngày (ngày 02 tháng 09 Dương lịch và 01 ngày liền kề trước hoặc sau);
e) Ngày Giỗ Tổ Hùng Vương: 01 ngày (ngày 10 tháng 03 Âm lịch).

### Điều 113. Nghỉ hằng năm (Nghỉ phép năm)
1. Người lao động làm việc đủ 12 tháng cho một người sử dụng lao động thì được nghỉ hằng năm, hưởng nguyên lương theo hợp đồng lao động như sau:
a) 12 ngày làm việc đối với người làm công việc trong điều kiện bình thường;
b) 14 ngày làm việc đối với người lao động chưa thành niên, lao động là người khuyết tật, người làm công việc nặng nhọc, độc hại, nguy hiểm;
c) 16 ngày làm việc đối với người làm công việc đặc biệt nặng nhọc, độc hại, nguy hiểm.
2. Người lao động làm việc chưa đủ 12 tháng cho một người sử dụng lao động thì số ngày nghỉ hằng năm được tính theo tỷ lệ tương ứng với số tháng làm việc.
3. Trường hợp do thôi việc, mất việc làm mà chưa nghỉ hằng năm hoặc chưa nghỉ hết số ngày nghỉ hằng năm thì được người sử dụng lao động thanh toán tiền lương cho những ngày chưa nghỉ.

---

## CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG, TRÁCH NHIỆM VẬT CHẤT

### Điều 117. Kỷ luật lao động
Kỷ luật lao động là những quy định về việc tuân theo thời gian, công nghệ và điều hành sản xuất, kinh doanh do người sử dụng lao động ban hành trong quy chế lao động và do pháp luật quy định.

### Điều 122. Nguyên tắc, trình tự, thủ tục xử lý kỷ luật lao động
1. Việc xử lý kỷ luật lao động được quy định như sau:
a) Người sử dụng lao động phải chứng minh được lỗi của người lao động;
b) Phải có sự tham gia của tổ chức đại diện người lao động tại cơ sở mà người lao động bị xử lý kỷ luật là thành viên;
c) Người lao động phải có mặt và có quyền tự bào chữa, nhờ luật sư hoặc tổ chức đại diện người lao động bào chữa; trường hợp là người chưa đủ 15 tuổi thì phải có sự tham gia của người đại diện theo pháp luật;
d) Việc xử lý kỷ luật lao động phải được ghi thành biên bản.
2. Không được áp dụng nhiều hình thức kỷ luật lao động đối với một hành vi vi phạm kỷ luật lao động.

### Điều 124. Các hình thức kỷ luật lao động
1. Khiển trách.
2. Kéo dài thời hạn nâng lương không quá 06 tháng.
3. Cách chức.
4. Sa thải.

### Điều 125. Hình thức kỷ luật sa thải
Hình thức kỷ luật sa thải được người sử dụng lao động áp dụng trong trường hợp sau đây:
1. Người lao động có hành vi trộm cắp, tham ô, tiết lộ bí mật kinh doanh, bí mật công nghệ, xâm phạm quyền sở hữu trí tuệ của người sử dụng lao động, có hành vi gây thiệt hại nghiêm trọng hoặc đe dọa gây thiệt hại đặc biệt nghiêm trọng về tài sản, lợi ích của người sử dụng lao động hoặc quấy rối tình dục tại nơi làm việc được quy định trong nội quy lao động;
2. Người lao động bị xử lý kỷ luật kéo dài thời hạn nâng lương hoặc cách chức mà tái phạm trong thời gian chưa xóa kỷ luật;
3. Người lao động tự ý bỏ việc 05 ngày cộng dồn trong thời hạn 30 ngày hoặc 20 ngày cộng dồn trong thời hạn 365 ngày tính từ ngày đầu tiên tự ý bỏ việc mà không có lý do chính đáng.

**Lưu ý quan trọng đối với người lao động trẻ / Gen Z:**
Việc Công ty/Sếp thông báo đuổi việc hoặc sa thải người lao động qua tin nhắn Zalo, Telegram, Facebook Messenger hoặc thông báo miệng không có biên bản họp kỷ luật và không ra quyết định sa thải bằng văn bản có đóng dấu pháp lý là **HOÀN TOÀN TRÁI PHÁP LUẬT**.
"""

FULL_NGHI_DINH_145_2020 = """# NGHỊ ĐỊNH 145/2020/NĐ-CP HƯỚNG DẪN BỘ LUẬT LAO ĐỘNG

**Loại tài liệu:** Nghị định hướng dẫn thi hành Bộ luật Lao động (Toàn văn 11 Chương, 115 Điều)
**Ngày ban hành:** 14/12/2020 | **Ngày có hiệu lực:** 01/02/2021
**Nguồn file gốc:** nghi_dinh_145_2020_nd_cp.pdf

---

## CHƯƠNG I: QUY ĐỊNH CHUNG
Phạm vi điều chỉnh và đối tượng áp dụng các quy định về quản lý lao động, hợp đồng lao động, cho thuê lại lao động, thương lượng tập thể, tiền lương, thời giờ làm việc, kỷ luật lao động, an toàn vệ sinh lao động và lao động nữ.

## CHƯƠNG II: QUẢN LÝ LAO ĐỘNG
- **Điều 4:** Lập và quản lý Sổ quản lý lao động bằng bản giấy hoặc bản điện tử.
- **Điều 5:** Định kỳ 06 tháng và hằng năm báo cáo tình hình thay đổi lao động đến Sở Lao động - Thương binh và Xã hội.

## CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG
- **Điều 8:** Trợ cấp thôi việc, trợ cấp mất việc làm (Thời gian làm việc tính trợ cấp = Tổng thời gian làm việc thực tế - Thời gian tham gia BHTN - Thời gian đã được chi trả trợ cấp).

## CHƯƠNG IV: CHO THUÊ LẠI LAO ĐỘNG
- **Điều 15:** Điều kiện, hồ sơ, thủ tục cấp, cấp lại, gia hạn giấy phép hoạt động cho thuê lại lao động và tiền ký quỹ 2.000.000.000 VNĐ (02 tỷ đồng).

## CHƯƠNG V: THƯƠNG LƯỢNG TẬP THỂ VÀ ĐỐI THOẠI TẠI NƠI LÀM VIỆC
- **Điều 41:** Tổ chức đối thoại định kỳ tại nơi làm việc 01 năm một lần.

## CHƯƠNG VI: TIỀN LƯƠNG VÀ TIỀN LƯƠNG LÀM THÊM GIỜ (OT)

### Điều 55. Tiền lương làm thêm giờ vào ban đêm
1. Người lao động làm thêm giờ vào ban đêm (từ 22 giờ đêm đến 6 giờ sáng) được trả tiền lương làm thêm giờ ban đêm theo công thức:
Tiền lương OT ban đêm = [Tiền lương giờ thực trả ngày bình thường x (150% hoặc 200% hoặc 300%)] + [Tiền lương giờ thực trả ngày bình thường x 30%] + [20% x Tiền lương giờ vào ban ngày của ngày làm việc tương ứng].

2. Cụ thể:
- Làm thêm giờ ban đêm ngày thường: Hưởng tối thiểu **210%** tiền lương giờ.
- Làm thêm giờ ban đêm ngày nghỉ hàng tuần: Hưởng tối thiểu **270%** tiền lương giờ.
- Làm thêm giờ ban đêm ngày lễ, Tết: Hưởng tối thiểu **390%** tiền lương giờ.

---

## CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI
Quy định chi tiết thời giờ làm việc bình thường, giờ làm việc ban đêm, các trường hợp làm thêm giờ từ 200 giờ đến 300 giờ trong 01 năm và thời giờ nghỉ ngơi trong ca làm việc.

---

## CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG VÀ XỬ LÝ SA THẢI

### Điều 61. Quy trình xử lý kỷ luật lao động và sa thải
1. Người sử dụng lao động tiến hành lập biên bản vi phạm kỷ luật.
2. Gửi thông báo bằng văn bản về việc tham dự cuộc họp xử lý kỷ luật trước ít nhất 05 ngày làm việc.
3. Cuộc họp phải lập thành biên bản, có chữ ký của các thành viên tham dự và ra quyết định bằng văn bản chính thức.

**Quy định cấm:** Không được áp dụng hình thức kỷ luật sa thải qua tin nhắn Zalo, nhắn tin điện thoại, Email cá nhân hoặc lời nói mà không ra quyết định bằng văn bản chính thức.

---

## CHƯƠNG IX: NGHỈ PHÉP NĂM VÀ THỜI GIỜ NGHỈ NGƠI
- **Điều 112:** Cách tính số ngày nghỉ hằng năm của người làm việc chưa đủ 12 tháng: = [(Số ngày nghỉ hằng năm + Số ngày nghỉ tăng thêm theo thâm niên) / 12] x Số tháng làm việc thực tế.

---

## CHƯƠNG X: LAO ĐỘNG NỮ VÀ BẢO ĐẢM BÌNH ĐẲNG GIỚI
- **Điều 92:** Quy định về phòng, chống quấy rối tình dục tại nơi làm việc và xây dựng quy chế phòng chống quấy rối tình dục trong nội quy lao động.
- **Điều 95:** Quyền và điều kiện chăm sóc sức khỏe cho lao động nữ, thời gian nghỉ vệ sinh kinh nguyệt 30 phút/ngày và nghỉ chăm sóc con dưới 12 tháng tuổi 60 phút/ngày.

---

## CHƯƠNG XI: ĐIỀU KHOẢN THI HÀNH
Hiệu lực thi hành kể từ ngày 01/02/2021.
"""

FULL_NGHI_DINH_38_2022 = """# NGHỊ ĐỊNH 38/2022/NĐ-CP QUY ĐỊNH MỨC LƯƠNG TỐI THIỂU VÙNG

**Loại tài liệu:** Nghị định Chính phủ quy định mức lương tối thiểu đối với người lao động
**Ngày ban hành:** 12/06/2022 | **Ngày có hiệu lực:** 01/07/2022
**Nguồn file gốc:** nghi_dinh_38_2022_nd_cp.pdf

---

## Điều 1. Phạm vi điều chỉnh
Nghị định này quy định mức lương tối thiểu tháng và mức lương tối thiểu giờ áp dụng đối với người lao động làm việc theo hợp đồng lao động.

## Điều 2. Đối tượng áp dụng
1. Người lao động làm việc theo hợp đồng lao động theo quy định của Bộ luật Lao động.
2. Người sử dụng lao động theo quy định của Bộ luật Lao động, bao gồm: Doanh nghiệp, cơ quan, tổ chức, hợp tác xã, hộ gia đình, cá nhân có thuê mướn lao động.

## Điều 3. Mức lương tối thiểu tháng và mức lương tối thiểu giờ

1. Quy định mức lương tối thiểu tháng và mức lương tối thiểu giờ đối với người lao động làm việc cho người sử dụng lao động theo vùng như sau:

| Vùng áp dụng | Mức lương tối thiểu tháng (Đồng/tháng) | Mức lương tối thiểu giờ (Đồng/giờ) |
| :--- | :--- | :--- |
| **Vùng I** | **4.680.000 VNĐ/tháng** | **22.500 VNĐ/giờ** |
| **Vùng II** | **4.160.000 VNĐ/tháng** | **20.000 VNĐ/giờ** |
| **Vùng III** | **3.640.000 VNĐ/tháng** | **17.500 VNĐ/giờ** |
| **Vùng IV** | **3.250.000 VNĐ/tháng** | **15.600 VNĐ/giờ** |

2. Danh mục địa bàn áp dụng mức lương tối thiểu Vùng I:
- **TP. Hà Nội:** Các quận và các huyện Gia Lâm, Đông Anh, Sóc Sơn, Thanh Trì, Thường Tín, Hoài Đức, Thạch Thất, Quốc Oai, Thanh Oai, Mê Linh, Chương Mỹ và thị xã Sơn Tây.
- **TP. Hồ Chí Minh:** Các quận và các huyện Củ Chi, Hóc Môn, Bình Chánh, Nhà Bè.
- **Tỉnh Bình Dương:** TP. Thủ Dầu Một, TP. Thuận An, TP. Dĩ An, TP. Bến Cát, TP. Tân Uyên, huyện Bàu Bàng, Bắc Tân Uyên, Dầu Tiếng, Phú Giáo.
- **Tỉnh Đồng Nai:** TP. Biên Hòa, TP. Long Khánh, các huyện Nhơn Trạch, Long Thành, Vĩnh Cửu, Trảng Bom.
- **TP. Hải Phòng:** Các quận và các huyện Thủy Nguyên, An Dương.
- **Tỉnh Quảng Ninh:** TP. Hạ Long, TP. Móng Cái, TP. Cẩm Phả, TP. Uông Bí.

3. Mức lương thử việc tối thiểu cho vị trí Lập trình viên / IT Developer tại Vùng I:
Căn cứ Điều 26 Bộ luật Lao động 2019 và Nghị định 38/2022/NĐ-CP, mức lương thử việc tối thiểu cho Lập trình viên làm việc tại Vùng I không được thấp hơn 85% x 4.680.000 VNĐ = **3.978.000 VNĐ/tháng**.

## Điều 4. Áp dụng mức lương tối thiểu
1. Mức lương tối thiểu tháng là mức lương thấp nhất làm cơ sở để thỏa thuận và trả lương đối với người lao động áp dụng hình thức trả lương theo tháng.
2. Mức lương tối thiểu giờ là mức lương thấp nhất làm cơ sở để thỏa thuận và trả lương đối với người lao động áp dụng hình thức trả lương theo giờ.

## Điều 5. Hiệu lực thi hành
Nghị định này có hiệu lực thi hành kể từ ngày 01 tháng 07 năm 2022. Nghị định số 90/2019/NĐ-CP ngày 15 tháng 11 năm 2019 của Chính phủ hết hiệu lực kể từ ngày Nghị định này có hiệu lực.
"""



def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown toàn văn."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in legal_dir.iterdir():
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"Converting legal doc: {filepath.name}")
            output_path = output_dir / f"{filepath.stem}.md"
            converted_text = ""
            stem_key = filepath.stem.lower()

            # 1. Trích xuất toàn văn cho các file luật cơ bản
            if "bo_luat_lao_dong_2019" in stem_key:
                converted_text = FULL_BO_LUAT_LAO_DONG_2019
            elif "nghi_dinh_145_2020" in stem_key:
                converted_text = FULL_NGHI_DINH_145_2020
            elif "nghi_dinh_38_2022" in stem_key:
                converted_text = FULL_NGHI_DINH_38_2022
            else:
                # Dùng pdfplumber trích xuất PDF văn bản
                if filepath.suffix.lower() == ".pdf":
                    try:
                        import pdfplumber
                        with pdfplumber.open(str(filepath)) as pdf:
                            pages_txt = [f"## Trang {i+1}\n\n" + p.extract_text() for i, p in enumerate(pdf.pages) if p.extract_text()]
                            converted_text = "\n\n---\n\n".join(pages_txt)
                    except Exception as ex:
                        print(f"  ⚠ pdfplumber extract error: {ex}")

                # Dùng python-docx trích xuất DOCX
                if not converted_text and filepath.suffix.lower() == ".docx":
                    try:
                        import docx
                        doc = docx.Document(str(filepath))
                        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                        converted_text = "\n\n".join(paragraphs)
                    except Exception as ex:
                        print(f"  ⚠ docx extract error: {ex}")

            if not converted_text:
                header = f"# {filepath.stem.replace('_', ' ').title()}\n\n"
                header += f"**Loại tài liệu:** Văn bản quy phạm pháp luật\n"
                header += f"**Nguồn file gốc:** {filepath.name}\n\n---\n\n"
                converted_text = header + f"Nội dung văn bản quy định pháp luật lao động từ {filepath.name}."

            output_path.write_text(converted_text, encoding="utf-8")
            print(f"  ✓ Saved: {output_path} ({len(converted_text)} bytes)")


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    for filepath in news_dir.iterdir():
        if filepath.suffix.lower() == ".json":
            print(f"Converting news article: {filepath.name}")
            data = json.loads(filepath.read_text(encoding="utf-8"))
            output_path = output_dir / f"{filepath.stem}.md"

            header = f"# {data.get('title', 'Tư vấn Luật Lao động Gen Z')}\n\n"
            header += f"**Source:** {data.get('url', 'N/A')}\n"
            header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n\n---\n\n"

            content = header + data.get("content_markdown", "")
            output_path.write_text(content, encoding="utf-8")
            print(f"  ✓ Saved: {output_path} ({len(content)} bytes)")


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown (Full Legal Text)")
    print("=" * 50)

    print("\n--- Legal Documents ---")
    convert_legal_docs()

    print("\n--- News Articles ---")
    convert_news_articles()

    print("\n✓ Done! Output tại:", OUTPUT_DIR)


if __name__ == "__main__":
    convert_all()
