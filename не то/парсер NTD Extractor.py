import re
import json

class NTDParser:
    def __init__(self):
        # Словарь ключевых параметров, которые мы ищем в тексте
        self.target_parameters = {
            "pressure": ["давление", "рабочее давление", "МПа"],
            "temperature": ["температура", "температурный режим", "градус", "°C"],
            "thickness": ["толщина стенки", "утонение", "мм"],
            "corrosion": ["скорость коррозии", "глубина коррозии", "мм/год"]
        }
        
        # Паттерны ограничений (Regex)
        # Ищет фразы вида: "не более 5.5", "не менее 10", "свыше 100"
        self.constraint_patterns = [
            r"(не более|не менее|свыше|до|от)\s+(\d+[.,]?\d*)\s*(МПа|мм|°C|%)",
            r"(должно быть|должна составлять)\s+(\d+[.,]?\d*)\s*(МПа|мм|°C|%)"
        ]

    def normalize_value(self, value_str):
        """Преобразует строку '5,5' в float 5.5"""
        return float(value_str.replace(',', '.'))

    def parse_text(self, text, source_doc_name):
        """
        Сканирует текст и извлекает правила.
        """
        found_rules = []
        
        # Разбиваем текст на предложения
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        
        for sentence in sentences:
            for param_key, keywords in self.target_parameters.items():
                # Если в предложении есть ключевое слово (напр. "давление")
                if any(k in sentence.lower() for k in keywords):
                    
                    # Ищем числовые ограничения
                    for pattern in self.constraint_patterns:
                        match = re.search(pattern, sentence, re.IGNORECASE)
                        if match:
                            operator_str = match.group(1).lower()
                            value = self.normalize_value(match.group(2))
                            unit = match.group(3)
                            
                            # Интерпретация оператора
                            rule_type = "MAX" if "не более" in operator_str or "до" in operator_str else \
                                        "MIN" if "не менее" in operator_str or "свыше" in operator_str else "EQUAL"

                            rule = {
                                "source": source_doc_name,
                                "parameter": param_key,
                                "original_text": sentence.strip(),
                                "constraint_type": rule_type,
                                "limit_value": value,
                                "unit": unit
                            }
                            found_rules.append(rule)
                            break # Правило найдено, идем к следующему предложению
                            
        return found_rules

# --- ТЕСТИРОВАНИЕ НА ПРИМЕРЕ ИЗ СП 284 ---

text_sp284 = """
6.1.2 Рабочее давление в промысловых трубопроводах не должно превышать проектное значение. 
Для трубопроводов класса I рабочее давление должно быть не более 10,0 МПа.
Температура перекачиваемого продукта должна быть не менее 5 °C во избежание парафинизации.
"""

parser = NTDParser()
rules = parser.parse_text(text_sp284, "СП 284.1325800.2016")

print(json.dumps(rules, indent=2, ensure_ascii=False))