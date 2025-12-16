import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math
import io

# ==========================================
# 1. ЯДРО РАСЧЕТА (КЛАСС)
# ==========================================
class PipeDefect:
    def __init__(self, L, d, t, D, SMYS, MAOP):
        self.L, self.d, self.t = float(L), float(d), float(t)
        self.D, self.SMYS, self.MAOP = float(D), float(SMYS), float(MAOP)

    def calculate_b31g_modified(self):
        # Защита от некорректных данных
        if self.t <= 0 or self.D <= 0: return {"erf": 0, "status": "ERROR"}
        
        if self.d >= self.t:
            return {"erf": 10.0, "p_safe": 0, "status": "УТЕЧКА"}
            
        z = (self.L ** 2) / (self.D * self.t)
        M = math.sqrt(1 + 0.6275 * z - 0.003375 * (z**2)) if z <= 50 else 0.032 * z + 3.3
        S_flow = self.SMYS + 69.0
        
        term1 = (2 * S_flow * self.t) / self.D
        d_t = self.d / self.t
        
        # Защита деления на ноль
        denom = (1 - 0.85 * d_t / M)
        if denom == 0: denom = 0.001
            
        p_safe = term1 * ((1 - 0.85 * d_t) / denom)
        
        erf = self.MAOP / p_safe if p_safe > 0 else 10.0
        
        status = "CRITICAL" if erf >= 1.0 else "WARNING" if erf >= 0.9 else "SAFE"
        
        return {
            "erf": round(erf, 3), 
            "p_safe": round(p_safe, 2), 
            "status": status
        }

# ==========================================
# 2. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================
def generate_sample_excel():
    """Генерирует тестовый журнал ВТД для демонстрации"""
    data = {
        'KM_Odometer': np.linspace(0, 50, 100), # 50 км трубы
        'Defect_ID': [f'DEF-{i:04d}' for i in range(100)],
        'Length_mm': np.random.uniform(10, 200, 100),
        'Depth_mm': np.random.uniform(0.5, 6.0, 100), # Некоторые глубокие
        'Wall_Thickness_mm': [12.0]*100,
        'Diameter_mm': [720.0]*100,
        'SMYS_MPa': [360.0]*100,
        'MAOP_MPa': [5.5]*100,
        # Имитация координат (вокруг Иркутска/Сибири для примера)
        'LAT': np.linspace(52.28, 52.50, 100) + np.random.normal(0, 0.001, 100),
        'LON': np.linspace(104.28, 104.50, 100) + np.random.normal(0, 0.001, 100)
    }
    df = pd.DataFrame(data)
    # Искусственно создаем пару критических дефектов
    df.loc[10, 'Depth_mm'] = 10.5 # Почти сквозной
    df.loc[45, 'Length_mm'] = 450.0 # Очень длинный
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return buffer

def batch_process(df):
    """Массовый расчет DataFrame"""
    results = []
    for index, row in df.iterrows():
        defect = PipeDefect(
            row['Length_mm'], row['Depth_mm'], row['Wall_Thickness_mm'],
            row['Diameter_mm'], row['SMYS_MPa'], row['MAOP_MPa']
        )
        res = defect.calculate_b31g_modified()
        results.append(res)
    
    res_df = pd.DataFrame(results)
    final_df = pd.concat([df.reset_index(drop=True), res_df], axis=1)
    return final_df

# ==========================================
# 3. ИНТЕРФЕЙС (UI)
# ==========================================
st.set_page_config(page_title="Pipeline Integrity Twin", layout="wide", page_icon="🛢️")

st.title("🛢️ Цифровой Двойник: Аналитика и Прогноз")
st.markdown("---")

# Выбор режима работы
mode = st.radio("Выберите режим работы:", ["📂 Пакетная загрузка (ВТД Excel)", "🧮 Калькулятор (Одиночный дефект)"], horizontal=True)

if mode == "📂 Пакетная загрузка (ВТД Excel)":
    st.info("Загрузите Excel-файл с результатами внутритрубной диагностики. Система автоматически рассчитает ERF, Psafe и определит критичность.")
    
    col_u1, col_u2 = st.columns([1, 2])
    
    with col_u1:
        st.subheader("1. Загрузка данных")
        uploaded_file = st.file_uploader("Перетащите файл сюда (xlsx, csv)", type=['xlsx', 'csv'])
        
        st.markdown("**Нет файла?**")
        sample_data = generate_sample_excel()
        st.download_button(
            label="Скачать тестовый шаблон (.xlsx)",
            data=sample_data,
            file_name="sample_pipeline_data.xlsx",
            mime="application/vnd.ms-excel"
        )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.toast(f"Загружено {len(df)} строк данных.", icon="✅")
            
            # Кнопка запуска расчета
            if st.button("🚀 Запустить Анализ (B31G + AI)"):
                with st.spinner('Выполняется расчет прочности и оценка рисков...'):
                    # Расчет
                    processed_df = batch_process(df)
                    
                    # Разделение по цветам для карты
                    # Критические - красные, Опасные - желтые, Норма - зеленые
                    processed_df['color'] = processed_df['status'].map({
                        'CRITICAL': '#FF0000', # Red
                        'WARNING': '#xFFA500', # Orange
                        'SAFE': '#00FF00'      # Green
                    })
                    # Размер точки зависит от глубины
                    processed_df['size'] = processed_df['Depth_mm'] * 10 

                st.success("Расчет завершен!")
                
                # --- ДАШБОРД РЕЗУЛЬТАТОВ ---
                c1, c2, c3 = st.columns(3)
                critical_count = len(processed_df[processed_df['status'] == 'CRITICAL'])
                warning_count = len(processed_df[processed_df['status'] == 'WARNING'])
                
                c1.metric("Всего дефектов", len(processed_df))
                c2.metric("Требуют ремонта (ERF > 1.0)", critical_count, delta="Критично", delta_color="inverse")
                c3.metric("Мониторинг (ERF > 0.9)", warning_count, delta="Внимание", delta_color="off")

                # --- КАРТА (Мини-ГИС) ---
                st.subheader("🗺️ Геопространственный анализ (Web-GIS)")
                # Фильтруем данные для карты (нужны колонки lat/lon)
                if 'LAT' in processed_df.columns and 'LON' in processed_df.columns:
                    # Streamlit map требует колонок 'lat', 'lon' (в нижнем регистре)
                    map_df = processed_df.rename(columns={'LAT': 'lat', 'LON': 'lon'})
                    st.map(map_df, color='color', size='size')
                else:
                    st.warning("В файле нет колонок LAT/LON. Отображение на карте невозможно.")

                # --- ТАБЛИЦА ---
                st.subheader("📋 Детальный отчет")
                # Подсветка критических строк
                def highlight_critical(s):
                    return ['background-color: #ffcccc' if s.status == 'CRITICAL' else '' for _ in s]
                
                st.dataframe(processed_df.style.apply(highlight_critical, axis=1), use_container_width=True)

                # --- ЭКСПОРТ ДЛЯ ARCGIS ---
                st.subheader("💾 Экспорт")
                st.write("Скачайте файл для импорта в ArcGIS Pro (Add XY Data).")
                
                csv_buffer = processed_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Скачать результат (.csv) для ArcGIS",
                    data=csv_buffer,
                    file_name="integrity_results_arcgis.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Ошибка при обработке файла: {e}")
            st.info("Убедитесь, что файл содержит колонки: Length_mm, Depth_mm, Wall_Thickness_mm, Diameter_mm, SMYS_MPa, MAOP_MPa")

elif mode == "🧮 Калькулятор (Одиночный дефект)":
    # (Сюда вставьте код из предыдущего этапа для одиночного расчета, если нужно)
    st.write("Переключитесь на вкладку пакетной загрузки для работы с Excel.")
    # Для краткости я не дублирую код одиночного режима здесь, 
    # но в финальной версии его можно оставить во втором блоке if/else.