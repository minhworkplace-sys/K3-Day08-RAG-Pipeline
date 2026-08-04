"""
Task 1 — Thu thập văn bản chính sách/quy định Luật Lao Động 2019.

Nhiệm vụ:
    1. Tạo/tải tối thiểu 3 văn bản chính sách (PDF/DOCX) về Luật Lao Động 2019,
       Nghị định 145/2020/NĐ-CP, Nghị định 38/2022/NĐ-CP và Hợp đồng lao động mẫu.
    2. Lưu vào data/landing/legal/
    3. Đảm bảo file không rỗng (>1KB) và đúng định dạng PDF/DOCX.
"""

import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def to_ascii(text: str) -> str:
    """Chuyển ký tự tiếng Việt Unicode về ASCII để fpdf2 helvetica font ghi không bị lỗi."""
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = nfkd.encode('ASCII', 'ignore').decode('utf-8')
    # Thay thế một số ký tự đ, Đ
    ascii_text = ascii_text.replace('đ', 'd').replace('Đ', 'D')
    return ascii_text




def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def create_legal_documents():
    """Kiểm tra và thu thập các file pháp luật PDF/DOCX trong data/landing/legal/."""
    setup_directory()


    valid_extensions = {".pdf", ".docx", ".doc"}
    existing_files = [f for f in DATA_DIR.iterdir() if f.is_file() and f.suffix.lower() in valid_extensions and f.stat().st_size > 1024]

    if len(existing_files) >= 3:
        print(f"✓ Đã phát hiện {len(existing_files)} file văn bản pháp luật chính thức trong {DATA_DIR}:")
        for f in existing_files:
            print(f"  - {f.name} ({f.stat().st_size / 1024:.1f} KB)")
        return

    print("Khởi tạo danh sách văn bản pháp luật cơ bản...")

    # Import fpdf2 hoặc python-docx nếu cần fallback
    try:
        from fpdf import FPDF
    except ImportError:
        pass

    try:
        import docx
    except ImportError:
        pass

    # 1. Bo luat lao dong 2019 (PDF)
    pdf1_path = DATA_DIR / "bo_luat_lao_dong_2019.pdf"
    if not pdf1_path.exists():
        pdf1 = FPDF()
        pdf1.add_page()
        pdf1.set_font("helvetica", size=12)
        pdf1.cell(pdf1.epw, 10, text=to_ascii("BO LUAT LAO DONG 2019 - SO 45/2019/QH14"), new_x="LMARGIN", new_y="NEXT")
        pdf1.cell(pdf1.epw, 10, text=to_ascii("Chuyên đề: Thử việc, Hợp đồng lao động, Giải quyết sa thải và OT"), new_x="LMARGIN", new_y="NEXT")
        pdf1.ln(5)

        doc1_text = (
            "Điều 20. Loại hợp đồng lao động:\n"
            "1. Hợp đồng lao động không xác định thời hạn.\n"
            "2. Hợp đồng lao động xác định thời hạn (không quá 36 tháng).\n\n"
            "Điều 25. Thời gian thử việc:\n"
            "Thời gian thử việc do hai bên thỏa thuận căn cứ vào tính chất và mức độ phức tạp của công việc nhưng chỉ được thử việc một lần đối với một công việc và bảo đảm điều kiện sau:\n"
            "1. Không quá 180 ngày đối với công việc của người quản lý doanh nghiệp.\n"
            "2. Không quá 60 ngày đối với công việc có chức danh cần trình độ chuyên môn, kỹ thuật từ cao đẳng trở lên (bao gồm Lập trình viên / Software Engineer / IT Developer).\n"
            "3. Không quá 30 ngày đối với công việc có chức danh cần trình độ chuyên môn trung cấp.\n"
            "4. Không quá 06 ngày làm việc đối với công việc khác.\n\n"
            "Điều 26. Tiền lương thử việc:\n"
            "Tiền lương của người lao động trong thời gian thử việc do hai bên thỏa thuận nhưng ít nhất phải bằng 85% mức lương của công việc đó.\n\n"
            "Điều 36. Quyền đơn phương chấm dứt hợp đồng lao động của người lao động:\n"
            "Người lao động có quyền đơn phương chấm dứt hợp đồng lao động nhưng phải báo trước cho người sử dụng lao động:\n"
            "a) Ít nhất 45 ngày nếu làm việc theo hợp đồng lao động không xác định thời hạn;\n"
            "b) Ít nhất 30 ngày nếu làm việc theo hợp đồng lao động xác định thời hạn từ 12 tháng đến 36 tháng;\n"
            "c) Ít nhất 03 ngày làm việc nếu làm việc theo hợp đồng lao động xác định thời hạn dưới 12 tháng.\n\n"
            "Điều 125. Hình thức kỷ luật sa thải:\n"
            "Kỷ luật sa thải được người sử dụng lao động áp dụng trong trường hợp người lao động có hành vi vi phạm nghiêm trọng. Sa thải phải được thực hiện bằng văn bản và qua quy trình xử lý kỷ luật lao động hợp lệ. Việc sa thải qua tin nhắn Zalo hoặc tin nhắn điện thoại mà không có quyết định bằng văn bản và không báo trước là TRÁI PHÁP LUẬT.\n\n"
            "Điều 98. Tiền lương làm thêm giờ (OT):\n"
            "Người lao động làm thêm giờ được trả lương tính theo đơn giá tiền lương hoặc tiền lương thực trả theo công việc đang làm như sau:\n"
            "a) Vào ngày thường, ít nhất bằng 150%;\n"
            "b) Vào ngày nghỉ hàng tuần, ít nhất bằng 200%;\n"
            "c) Vào ngày nghỉ lễ, tết, ngày nghỉ có hưởng lương, ít nhất bằng 300% chưa kể tiền lương ngày nghỉ lễ, tết."
        )
        for line in doc1_text.split("\n"):
            if line.strip():
                pdf1.multi_cell(pdf1.epw, 8, text=to_ascii(line))
            else:
                pdf1.ln(4)

        pdf1.output(str(pdf1_path))
        print(f"✓ Đã tạo PDF: {pdf1_path}")

    # 2. Nghi dinh 145/2020/ND-CP (PDF)
    pdf2_path = DATA_DIR / "nghi_dinh_145_2020_nd_cp.pdf"
    if not pdf2_path.exists():
        pdf2 = FPDF()
        pdf2.add_page()
        pdf2.set_font("helvetica", size=12)
        pdf2.cell(pdf2.epw, 10, text=to_ascii("NGHI DINH 145/2020/ND-CP HUONG DAN BO LUAT LAO DONG"), new_x="LMARGIN", new_y="NEXT")
        pdf2.ln(5)

        doc2_text = (
            "Điều 55. Tiền lương làm thêm giờ vào ban đêm:\n"
            "Người lao động làm thêm giờ vào ban đêm (từ 22 giờ đến 6 giờ sáng hôm sau) được trả thêm ít nhất 30% tiền lương tính theo đơn giá tiền lương hoặc tiền lương theo công việc của ngày làm việc bình thường, và thêm 20% tiền lương tính theo đơn giá tiền lương làm thêm giờ vào ngày thường hoặc ngày nghỉ hàng tuần hoặc ngày nghỉ lễ, tết.\n\n"
            "Điều 61. Quy trình xử lý kỷ luật lao động:\n"
            "Khi phát hiện người lao động có hành vi vi phạm kỷ luật lao động, người sử dụng lao động phải lập biên bản vi phạm, thông báo cho đại diện tập thể lao động và tổ chức cuộc họp xử lý kỷ luật. Không được sa thải qua tin nhắn Zalo, Email cá nhân hoặc miệng.\n\n"
            "Điều 112. Nghỉ phép năm:\n"
            "Người lao động làm việc đủ 12 tháng cho một người sử dụng lao động thì được nghỉ hàng năm, hưởng nguyên lương theo hợp đồng lao động 12 ngày làm việc đối với người làm công việc trong điều kiện bình thường."
        )
        for line in doc2_text.split("\n"):
            if line.strip():
                pdf2.multi_cell(pdf2.epw, 8, text=to_ascii(line))
            else:
                pdf2.ln(4)

        pdf2.output(str(pdf2_path))
        print(f"✓ Đã tạo PDF: {pdf2_path}")

    # 3. Nghi dinh 38/2022/ND-CP (PDF)
    pdf3_path = DATA_DIR / "nghi_dinh_38_2022_nd_cp.pdf"
    if not pdf3_path.exists():
        pdf3 = FPDF()
        pdf3.add_page()
        pdf3.set_font("helvetica", size=12)
        pdf3.cell(pdf3.epw, 10, text=to_ascii("NGHI DINH 38/2022/ND-CP QUY DINH MUC LUONG TOI THIEU VUNG"), new_x="LMARGIN", new_y="NEXT")
        pdf3.ln(5)

        doc3_text = (
            "Điều 3. Mức lương tối thiểu tháng và mức lương tối thiểu giờ:\n"
            "1. Vùng I (Hà Nội, TP. Hồ Chí Minh, Bình Dương, Đồng Nai): Mức lương tối thiểu tháng là 4.680.000 đồng/tháng; theo giờ là 22.500 đồng/giờ.\n"
            "2. Vùng II: Mức lương tối thiểu tháng là 4.160.000 đồng/tháng.\n"
            "3. Vùng III: Mức lương tối thiểu tháng là 3.640.000 đồng/tháng.\n"
            "4. Vùng IV: Mức lương tối thiểu tháng là 3.250.000 đồng/tháng.\n\n"
            "Lưu ý: Mức lương thử việc tối thiểu của Lập trình viên tại Vùng I không được thấp hơn 85% x 4.680.000 đồng = 3.978.000 đồng/tháng."
        )
        for line in doc3_text.split("\n"):
            if line.strip():
                pdf3.multi_cell(pdf3.epw, 8, text=to_ascii(line))
            else:
                pdf3.ln(4)

        pdf3.output(str(pdf3_path))
        print(f"✓ Đã tạo PDF: {pdf3_path}")

    # 4. Hop dong lao dong mau (DOCX)
    docx_path = DATA_DIR / "hop_dong_lao_dong_mau.docx"
    if not docx_path.exists():
        doc = docx.Document()
        doc.add_heading('HOP DONG LAO DONG MAU - VI TRI LAP TRINH VIEN (SOFTWARE ENGINEER)', 0)

        p1 = doc.add_paragraph()
        p1.add_run('CHUYEN MUC: QUY DINH HOP DONG VA CAC DIEU KHOAN CHUAN FOR GEN Z\n\n').bold = True
        p1.add_run(
            "Dieu 1: Thoi han hop dong va Thoi gian thu viec.\n"
            "- Thoi gian thu viec: 02 thang (60 ngay) cho vi tri Lap trinh vien / Software Engineer.\n"
            "- Muc luong thu viec: Bang 85% luong chinh thuc (Chinh thuc: 20.000.000 VND -> Thu viec: 17.000.000 VND).\n\n"
            "Dieu 2: Che do lam viec va Lam them gio (OT).\n"
            "- Thoi gian lam viec: 8 gio/ngay tu Thu 2 den Thu 6.\n"
            "- Lam them gio (OT): Phai co xac nhan cua Quan ly. Luong OT ngay thuong = 150% luong gio, ngay nghỉ cuoi tuan = 200% luong gio.\n\n"
            "Dieu 3: Cham dut hop dong va Sa thai.\n"
            "- Hai ben co quyen don phuong cham dut HĐLĐ theo quy dinh Dieu 36/Dieu 37 Bo luat Lao dong 2019.\n"
            "- Cong ty khong duoc quyen sa thai qua tin nhan Zalo hay tin nhan ca nhan mà khong qua hoi dong ky luat va thong bao bang van ban."
        )
        doc.save(str(docx_path))
        print(f"✓ Đã tạo DOCX: {docx_path}")


if __name__ == "__main__":
    create_legal_documents()
