import streamlit as st

st.set_page_config(page_title="Tính Thuế TNCN", layout="wide")

st.title("Hệ thống tính Thuế Thu nhập cá nhân")

st.info("Mẫu khung ứng dụng Streamlit: tính thuế tháng, quyết toán năm, so sánh hoàn/nộp bổ sung. Cần rà soát lại các thông số pháp lý trước khi sử dụng thực tế.")

GTBT_THANG = 15_500_000
GTNPT_THANG = 6_200_000

def tax_monthly(income):
    if income <= 0:
        return 0
    brackets = [
        (10_000_000, 0.05),
        (30_000_000, 0.10),
        (60_000_000, 0.20),
        (100_000_000, 0.30),
        (float("inf"), 0.35),
    ]
    tax = 0
    lower = 0
    for upper, rate in brackets:
        if income > upper:
            tax += (upper - lower) * rate
            lower = upper
        else:
            tax += (income - lower) * rate
            break
    return tax

tab1, tab2, tab3 = st.tabs(["Thuế tháng", "Quyết toán năm", "Kết quả"])

with tab1:
    salary = st.number_input("Lương + phụ cấp tháng", min_value=0.0, value=20000000.0)
    dependents = st.number_input("Số người phụ thuộc", min_value=0, step=1)
    insurance = st.number_input("Bảo hiểm tháng", min_value=0.0, value=0.0)

    taxable_month = max(
        salary - insurance - GTBT_THANG - dependents * GTNPT_THANG,
        0
    )

    monthly_tax = tax_monthly(taxable_month)

    st.metric("Thu nhập tính thuế tháng", f"{taxable_month:,.0f}")
    st.metric("Thuế tạm khấu trừ tháng", f"{monthly_tax:,.0f}")

with tab2:
    annual_income = st.number_input("Tổng thu nhập năm", min_value=0.0, value=240000000.0)
    bonus = st.number_input("Thưởng cuối năm", min_value=0.0, value=0.0)
    annual_insurance = st.number_input("Bảo hiểm cả năm", min_value=0.0, value=0.0)

    annual_taxable = max(
        annual_income + bonus
        - annual_insurance
        - GTBT_THANG * 12
        - dependents * GTNPT_THANG * 12,
        0
    )

    annual_tax = tax_monthly(annual_taxable / 12) * 12

with tab3:
    withheld = monthly_tax * 12
    diff = annual_tax - withheld

    st.metric("Thuế đã khấu trừ trong năm", f"{withheld:,.0f}")
    st.metric("Thuế quyết toán năm", f"{annual_tax:,.0f}")
    st.metric("Chênh lệch", f"{diff:,.0f}")

    if diff > 0:
        st.error(f"Nộp bổ sung: {diff:,.0f} đồng")
    elif diff < 0:
        st.success(f"Được hoàn thuế: {abs(diff):,.0f} đồng")
    else:
        st.info("Không phát sinh chênh lệch")

