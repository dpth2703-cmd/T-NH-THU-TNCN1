import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính Thuế TNCN",
    page_icon="💰",
    layout="wide"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 CHƯƠNG TRÌNH TÍNH THUẾ THU NHẬP CÁ NHÂN")

st.write("Nhập đầy đủ thông tin để tính thuế TNCN.")

# =========================
# HẰNG SỐ
# =========================
GIAM_TRU_BAN_THAN = 15_500_000
GIAM_TRU_NPT = 6_200_000

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📌 Thu nhập")

col1, col2 = st.columns(2)

with col1:
    luong = st.number_input(
        "Lương cơ bản",
        min_value=0.0,
        value=15000000.0,
        step=100000.0
    )

    thuong = st.number_input(
        "Tiền thưởng",
        min_value=0.0,
        value=0.0,
        step=100000.0
    )

    phu_cap = st.number_input(
        "Tổng phụ cấp chịu thuế",
        min_value=0.0,
        value=0.0,
        step=100000.0
    )

with col2:
    tien_thue_nha = st.number_input(
        "Tiền thuê nhà công ty trả hộ",
        min_value=0.0,
        value=0.0,
        step=100000.0
    )

    thu_nhap_mien_thue = st.number_input(
        "Khoản miễn thuế",
        min_value=0.0,
        value=0.0,
        step=100000.0
    )

st.subheader("📌 Bảo hiểm")

col3, col4, col5 = st.columns(3)

with col3:
    bhxh = st.number_input(
        "BHXH",
        min_value=0.0,
        value=0.0
    )

with col4:
    bhyt = st.number_input(
        "BHYT",
        min_value=0.0,
        value=0.0
    )

with col5:
    bhtn = st.number_input(
        "BHTN",
        min_value=0.0,
        value=0.0
    )

st.subheader("📌 Giảm trừ")

so_npt = st.number_input(
    "Số người phụ thuộc",
    min_value=0,
    value=0,
    step=1
)

tu_thien = st.number_input(
    "Khoản từ thiện được khấu trừ",
    min_value=0.0,
    value=0.0
)

# =========================
# NÚT TÍNH
# =========================
if st.button("📊 TÍNH THUẾ"):

    # Thu nhập trước tiền thuê nhà
    thu_nhap_tam = (
        luong
        + thuong
        + phu_cap
        - thu_nhap_mien_thue
    )

    # Giới hạn tiền thuê nhà 15%
    gioi_han_nha = thu_nhap_tam * 0.15

    tien_nha_tinh_thue = min(
        tien_thue_nha,
        gioi_han_nha
    )

    # Thu nhập chịu thuế
    thu_nhap_chiu_thue = (
        thu_nhap_tam
        + tien_nha_tinh_thue
    )

    # Bảo hiểm
    tong_bao_hiem = (
        bhxh
        + bhyt
        + bhtn
    )

    # Giảm trừ gia cảnh
    giam_tru = (
        GIAM_TRU_BAN_THAN
        + so_npt * GIAM_TRU_NPT
    )

    # Thu nhập tính thuế
    thu_nhap_tinh_thue = (
        thu_nhap_chiu_thue
        - tong_bao_hiem
        - giam_tru
        - tu_thien
    )

    if thu_nhap_tinh_thue <= 0:

        st.success("Không phát sinh thuế TNCN")

    else:

        bac_thue = [
            (5000000, 0.05),
            (10000000, 0.10),
            (18000000, 0.15),
            (32000000, 0.20),
            (52000000, 0.25),
            (80000000, 0.30),
            (float("inf"), 0.35)
        ]

        thue = 0
        con_lai = thu_nhap_tinh_thue
        moc_duoi = 0

        for gioi_han, ty_le in bac_thue:

            muc = min(
                con_lai,
                gioi_han - moc_duoi
            )

            if muc <= 0:
                break

            thue += muc * ty_le

            con_lai -= muc
            moc_duoi = gioi_han

        luong_thuc_nhan = (
            thu_nhap_chiu_thue
            - tong_bao_hiem
            - thue
        )

        st.subheader("📋 KẾT QUẢ")

        st.metric(
            "Thu nhập chịu thuế",
            f"{thu_nhap_chiu_thue:,.0f} VNĐ"
        )

        st.metric(
            "Thu nhập tính thuế",
            f"{thu_nhap_tinh_thue:,.0f} VNĐ"
        )

        st.metric(
            "Thuế TNCN phải nộp",
            f"{thue:,.0f} VNĐ"
        )

        st.metric(
            "Lương thực nhận",
            f"{luong_thuc_nhan:,.0f} VNĐ"
        )

        st.info(
            f"Giảm trừ bản thân: {GIAM_TRU_BAN_THAN:,.0f} VNĐ | "
            f"Người phụ thuộc: {so_npt} người"
        )
