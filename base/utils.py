from docx import Document
from .models import Question, Question2
from docx import Document


def process_question_file(file_path):
    document = Document(file_path)
    questions = []
    question = None

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        
        # Phát hiện câu hỏi
        if text.startswith("Câu"):
            if question:  # Lưu câu hỏi trước đó
                questions.append(question)
            question = {
                "name": text.split(". ", 1)[1].strip(),
                "Ans_a": "",
                "Ans_b": "",
                "Ans_c": "",
                "Ans_d": "",
                "correct": None,
            }
        
        # Phát hiện các đáp án
        elif text.startswith("A.") or text.startswith("B.") or text.startswith("C.") or text.startswith("D."):
            key = f"Ans_{text[0].lower()}"  # "A." -> "Ans_a"
            answer_text = text[2:].strip()
            
            # Kiểm tra định dạng (in đậm, tô màu, v.v.)
            is_correct = any(run.bold or run.font.color for run in paragraph.runs)
            question[key] = answer_text
            if is_correct:
                question["correct"] = key
    
    # Lưu câu hỏi cuối cùng
    if question:
        questions.append(question)
    
    return questions

def save_questions_to_db(questions, question_type):
    if question_type == 1:  # Lưu vào Question
        for q in questions:
            Question.objects.create(
                name=q["name"],
                Ans_a=q["Ans_a"],
                Ans_b=q["Ans_b"],
                Ans_c=q["Ans_c"],
                Ans_d=q["Ans_d"],
                Corect_ans=q["Corect_ans"]
            )
    elif question_type == 2:  # Lưu vào Question2
        for q in questions:
            Question2.objects.create(
                name=q["name"],
                Ans_a=q["Ans_a"],
                Ans_b=q["Ans_b"],
                Ans_c=q["Ans_c"],
                Ans_d=q["Ans_d"],
                Corect_ans_a=q["Corect_ans_a"],
                Corect_ans_b=q["Corect_ans_b"],
                Corect_ans_c=q["Corect_ans_c"],
                Corect_ans_d=q["Corect_ans_d"]
            )