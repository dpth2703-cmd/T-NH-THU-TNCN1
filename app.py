import streamlit as st

st.set_page_config(page_title="Tính Thuế TNCN", layout="wide")

st.title("💰 PHẦN MỀM TÍNH THUẾ THU NHẬP CÁ NHÂN")

st.markdown("""
### Người phụ thuộc
Xem quy định tại Điều 9 Thông tư 111/2013/TT-BTC:

https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-111-2013-TT-BTC-huong-dan-Luat-thue-thu-nhap-ca-nhan-Luat-sua-doi-Luat-thue-thu-nhap-ca-nhan-212181.aspx
""")

# =========================
# THU NHẬP TỪ LƯƠNG
# =========================

st.header("1. Thu nhập từ tiền lương, tiền công")

luong = st.number_input(
    "A. Nhập tổng thu nhập từ lương + phụ cấp (VNĐ/năm)",
    min_value=0.0,
    step=1000000.0
)

# =========================
# NGƯỜI PHỤ THUỘC
# =========================

st.header("2. Người phụ thuộc")

nguoi_phu_thuoc = st.number_input(
    "B. Số người phụ thuộc",
    min_value=0,
    step=1
)

# =========================
# THU NHẬP KHÁC
# =========================

st.header("3. Thu nhập khác")

loai_thu_nhap = {
    "Trúng thưởng": 0.10,
    "Bản quyền": 0.05,
    "Nhượng quyền thương mại": 0.05,
    "Chuyển nhượng vốn": 0.001,
    "Cổ tức": 0.05,
    "Cho thuê tài sản": 0.05,
    "Thừa kế": 0.10,
    "Quà tặng": 0.10
}

so_nguon = st.number_input(
    "Số nguồn thu nhập khác",
    min_value=0,
    max_value=10,
    value=1
)

tong_thue_khac = 0
tong_thu_nhap_khac = 0

for i in range(int(so_nguon)):
    st.subheader(f"Nguồn thu nhập khác {i+1}")

    loai = st.selectbox(
        f"C{i+1}. Loại thu nhập",
        list(loai_thu_nhap.keys()),
        key=f"loai_{i}"
    )

    thu_nhap = st.number_input(
        f"D{i+1}. Giá trị thu nhập (VNĐ)",
        min_value=0.0,
        key=f"thu_nhap_{i}"
    )

    thue_suat = loai_thu_nhap[loai]

    tong_thu_nhap_khac += thu_nhap
    tong_thue_khac += thu_nhap * thue_suat

# =========================
# THƯỞNG CUỐI NĂM
# =========================

st.header("4. Thưởng cuối năm")

thuong = st.number_input(
    "E. Khoản thưởng cuối năm",
    min_value=0.0,
    step=1000000.0
)

# =========================
# BẢO HIỂM
# =========================

st.header("5. Khấu trừ bảo hiểm")

luong_co_so = st.number_input(
    "Mức lương cơ sở hiện hành",
    value=2340000.0
)

bao_hiem = st.number_input(
    "Số tiền bảo hiểm được khấu trừ",
    min_value=0.0
)

gioi_han_bao_hiem = luong_co_so * 20

bao_hiem_duoc_tru = min(
    bao_hiem,
    gioi_han_bao_hiem
)

# =========================
# TÍNH THUẾ LŨY TIẾN
# =========================

def tinh_thue_luy_tien(thu_nhap):
    bac_thue = [
        (60000000, 0.05),
        (60000000, 0.10),
        (96000000, 0.15),
        (168000000, 0.20),
        (240000000, 0.25),
        (336000000, 0.30),
        (float("inf"), 0.35)
    ]

    thue = 0
    con_lai = thu_nhap

    for muc, ty_le in bac_thue:
        if con_lai <= 0:
            break

        tinh_phan = min(con_lai, muc)
        thue += tinh_phan * ty_le
        con_lai -= tinh_phan

    return thue

# =========================
# NÚT TÍNH TOÁN
# =========================

if st.button("TÍNH THUẾ TNCN"):

    giam_tru_ban_than = 132000000
    giam_tru_nguoi_phu_thuoc = nguoi_phu_thuoc * 52800000

    tong_thu_nhap = (
        luong
        + thuong
    )

    thu_nhap_tinh_thue = (
        tong_thu_nhap
        - giam_tru_ban_than
        - giam_tru_nguoi_phu_thuoc
        - bao_hiem_duoc_tru
    )

    thu_nhap_tinh_thue = max(0, thu_nhap_tinh_thue)

    thue_luong = tinh_thue_luy_tien(
        thu_nhap_tinh_thue
    )

    tong_thue = thue_luong + tong_thue_khac

    st.success("KẾT QUẢ TÍNH THUẾ")

    st.write(f"**Tổng thu nhập lương + thưởng:** {tong_thu_nhap:,.0f} VNĐ")

    st.write(f"**Tổng thu nhập khác:** {tong_thu_nhap_khac:,.0f} VNĐ")

    st.write(f"**Giảm trừ bản thân:** {giam_tru_ban_than:,.0f} VNĐ")

    st.write(f"**Giảm trừ người phụ thuộc:** {giam_tru_nguoi_phu_thuoc:,.0f} VNĐ")

    st.write(f"**Bảo hiểm được trừ:** {bao_hiem_duoc_tru:,.0f} VNĐ")

    st.write(f"**Thu nhập tính thuế:** {thu_nhap_tinh_thue:,.0f} VNĐ")

    st.write(f"**Thuế từ tiền lương, tiền công:** {thue_luong:,.0f} VNĐ")

    st.write(f"**Thuế từ thu nhập khác:** {tong_thue_khac:,.0f} VNĐ")

    st.subheader(
        f"💵 TỔNG THUẾ PHẢI NỘP: {tong_thue:,.0f} VNĐ"
    )
