```python
import streamlit as st

st.set_page_config(
    page_title="Tính Thuế TNCN",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Chương Trình Tính Thuế Thu Nhập Cá Nhân")

# ======================
# HẰNG SỐ
# ======================

GIAM_TRU_BAN_THAN = 15_500_000
GIAM_TRU_NGUOI_PHU_THUOC = 6_200_000

# ======================
# NHẬP DỮ LIỆU
# ======================

st.header("Thông tin thu nhập")

col1, col2 = st.columns(2)

with col1:
    luong_co_ban = st.number_input(
        "Lương cơ bản (VNĐ)",
        min_value=0.0,
        value=15000000.0
    )

    thuong = st.number_input(
        "Tiền thưởng (VNĐ)",
        min_value=0.0,
        value=0.0
    )

    phu_cap_chuc_vu = st.number_input(
        "Phụ cấp chức vụ",
        min_value=0.0,
        value=0.0
    )

    phu_cap_trach_nhiem = st.number_input(
        "Phụ cấp trách nhiệm",
        min_value=0.0,
        value=0.0
    )

with col2:
    phu_cap_dien_thoai = st.number_input(
        "Phụ cấp điện thoại",
        min_value=0.0,
        value=0.0
    )

    phu_cap_xang_xe = st.number_input(
        "Phụ cấp xăng xe",
        min_value=0.0,
        value=0.0
    )

    tien_thue_nha = st.number_input(
        "Tiền thuê nhà công ty trả hộ",
        min_value=0.0,
        value=0.0
    )

st.header("Bảo hiểm")

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

st.header("Giảm trừ")

so_nguoi_phu_thuoc = st.number_input(
    "Số người phụ thuộc",
    min_value=0,
    step=1
)

tu_thien = st.number_input(
    "Khoản từ thiện / khuyến học",
    min_value=0.0,
    value=0.0
)

# ======================
# NÚT TÍNH
# ======================

if st.button("📊 TÍNH THUẾ"):

    thu_nhap_chiu_thue_tam = (
        luong_co_ban
        + thuong
        + phu_cap_chuc_vu
        + phu_cap_trach_nhiem
        + phu_cap_dien_thoai
        + phu_cap_xang_xe
    )

    gioi_han_thue_nha = thu_nhap_chiu_thue_tam * 0.15

    tien_thue_nha_chiu_thue = min(
        tien_thue_nha,
        gioi_han_thue_nha
    )

    thu_nhap_chiu_thue = (
        thu_nhap_chiu_thue_tam
        + tien_thue_nha_chiu_thue
    )

    tong_bao_hiem = bhxh + bhyt + bhtn

    giam_tru_gia_canh = (
        GIAM_TRU_BAN_THAN
        + so_nguoi_phu_thuoc * GIAM_TRU_NGUOI_PHU_THUOC
    )

    thu_nhap_tinh_thue = (
        thu_nhap_chiu_thue
        - tong_bao_hiem
        - giam_tru_gia_canh
        - tu_thien
    )

    if thu_nhap_tinh_thue <= 0:
        st.success("Không phát sinh thuế TNCN")
    else:

        bac_thue = [
            (5_000_000, 0.05),
            (10_000_000, 0.10),
            (18_000_000, 0.15),
            (32_000_000, 0.20),
            (52_000_000, 0.25),
            (80_000_000, 0.30),
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

        thuc_nhan = (
            thu_nhap_chiu_thue
            - tong_bao_hiem
            - thue
        )

        st.subheader("📋 Kết quả")

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
            f"{thuc_nhan:,.0f} VNĐ"
        )
```
