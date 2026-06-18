import streamlit as st

st.set_page_config(page_title="Tính Thuế TNCN 2026", layout="wide")

st.title("💰 ỨNG DỤNG TÍNH THUẾ THU NHẬP CÁ NHÂN (TNCN) - QUYẾT TOÁN NĂM")

# =========================
# CONFIG LUẬT
# =========================

GIAM_TRU_BAN_THAN = 15_500_000
GIAM_TRU_PHU_THUOC = 6_600_000
THUE_TRUNG_THUONG_GIAM = 10_000_000

# =========================
# BIỂU THUẾ THÁNG (lũy tiến)
# =========================

def tinh_thue_luy_tien(thu_nhap):
    bac = [
        (5_000_000, 0.05),
        (5_000_000, 0.10),
        (8_000_000, 0.15),
        (14_000_000, 0.20),
        (20_000_000, 0.25),
        (28_000_000, 0.30),
        (float("inf"), 0.35)
    ]

    thue = 0
    for muc, rate in bac:
        if thu_nhap <= 0:
            break
        tinh = min(muc, thu_nhap)
        thue += tinh * rate
        thu_nhap -= tinh

    return thue

# =========================
# INPUT
# =========================

st.header("1. Thu nhập từ lương")

luong_thang = st.number_input("A. Thu nhập lương + phụ cấp / tháng", 0.0, step=1000000.0)

st.header("2. Người phụ thuộc")

nguoi_phu_thuoc = st.number_input("B. Số người phụ thuộc", 0, step=1)

st.header("3. Thu nhập khác")

so_nguon = st.number_input("Số nguồn thu nhập khác", 0, 10, 1)

thu_nhap_khac_nam = 0
thue_khac_nam = 0

thu_nhap_khac_thang = 0
thue_khac_thang = 0

loai_thu_nhap = {
    "Trúng thưởng": 0.10,
    "Bản quyền": 0.05,
    "Nhượng quyền": 0.05,
    "Cổ tức": 0.05,
    "Chuyển nhượng vốn": 0.001,
    "Quà tặng": 0.10,
    "Thừa kế": 0.10
}

for i in range(int(so_nguon)):
    st.subheader(f"Nguồn thu nhập {i+1}")

    loai = st.selectbox(
        f"Loại thu nhập {i+1}",
        list(loai_thu_nhap.keys()),
        key=f"loai_{i}"
    )

    tien = st.number_input(
        f"Số tiền nguồn {i+1}",
        0.0,
        step=1000000.0,
        key=f"tien_{i}"
    )

    thue_suat = loai_thu_nhap[loai]

    # TRÚNG THƯỞNG: có số vé
    if loai == "Trúng thưởng":
        so_ve = st.number_input(
            f"Số vé trúng thưởng {i+1}",
            min_value=1,
            value=1,
            key=f"ve_{i}"
        )

        thu_nhap_chiu_thue = max(0, (tien - THUE_TRUNG_THUONG_GIAM) * so_ve)
    else:
        thu_nhap_chiu_thue = tien

    thue = thu_nhap_chiu_thue * thue_suat

    thu_nhap_khac_nam += thu_nhap_chiu_thue * 12
    thue_khac_nam += thue * 12

    thu_nhap_khac_thang += thu_nhap_chiu_thue
    thue_khac_thang += thue

st.header("4. Thưởng cuối năm")

thuong = st.number_input("E. Thưởng cuối năm", 0.0, step=1000000.0)

st.header("5. Số tháng làm việc")

so_thang = st.number_input("Số tháng trong năm (1-12)", 1, 12, 12)

# =========================
# TÍNH TOÁN
# =========================

if st.button("🚀 TÍNH THUẾ TNCN"):

    # ===== THÁNG =====
    giam_tru_thang = GIAM_TRU_BAN_THAN + nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC

    thu_nhap_tinh_thue_thang = luong_thang - giam_tru_thang

    if thu_nhap_tinh_thue_thang < 0:
        thu_nhap_tinh_thue_thang = 0

    thue_luong_thang = tinh_thue_luy_tien(thu_nhap_tinh_thue_thang)

    thue_thang_total = thue_luong_thang + thue_khac_thang

    # ===== NĂM =====
    tong_luong_nam = luong_thang * so_thang + thuong

    giam_tru_nam = (
        GIAM_TRU_BAN_THAN * so_thang
        + nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC * so_thang
    )

    thu_nhap_tinh_thue_nam = (
        tong_luong_nam - giam_tru_nam
    )

    if thu_nhap_tinh_thue_nam < 0:
        thu_nhap_tinh_thue_nam = 0

    thue_luong_nam = tinh_thue_luy_tien(thu_nhap_tinh_thue_nam)

    tong_thue_da_khau_tru = thue_thang_total * so_thang

    tong_thue_phai_nop = thue_luong_nam + thue_khac_nam

    chenhlech = tong_thue_da_khau_tru - tong_thue_phai_nop

    # =========================
    # OUTPUT
    # =========================

    st.subheader("📊 KẾT QUẢ")

    st.write(f"Thu nhập tính thuế tháng: {thu_nhap_tinh_thue_thang:,.0f}")
    st.write(f"Thuế TNCN tháng: {thue_thang_total:,.0f}")

    st.write(f"Thu nhập tính thuế năm: {thu_nhap_tinh_thue_nam:,.0f}")
    st.write(f"Thuế phải nộp năm: {tong_thue_phai_nop:,.0f}")

    st.write(f"Thuế đã khấu trừ: {tong_thue_da_khau_tru:,.0f}")

    st.subheader("💡 QUYẾT TOÁN")

    if chenhlech > 0:
        st.success(f"🟢 HOÀN THUẾ: {chenhlech:,.0f} VNĐ")

    elif chenhlech < 0:
        st.error(f"🔴 PHẢI NỘP BỔ SUNG: {-chenhlech:,.0f} VNĐ")

    else:
        st.info("⚖️ KHÔNG PHÁT SINH THUẾ")
