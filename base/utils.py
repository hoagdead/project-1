from docx import Document
from .models import Question, Question2
from docx import Document

def process_question_file(file):
    document = Document(file)
    questions = []
    
    # Duyệt qua từng đoạn văn trong file Word
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text.startswith("Câu hỏi:"):
            question = {
                "name": text.replace("Câu hỏi:", "").strip(),
                "Ans_a": "",
                "Ans_b": "",
                "Ans_c": "",
                "Ans_d": "",
                "correct": None,
            }
        elif text.startswith("Đáp án A:"):
            question["Ans_a"] = text.replace("Đáp án A:", "").strip()
        elif text.startswith("Đáp án B:"):
            question["Ans_b"] = text.replace("Đáp án B:", "").strip()
        elif text.startswith("Đáp án C:"):
            question["Ans_c"] = text.replace("Đáp án C:", "").strip()
        elif text.startswith("Đáp án D:"):
            question["Ans_d"] = text.replace("Đáp án D:", "").strip()
        elif text.startswith("Đáp án đúng:"):
            question["correct"] = text.replace("Đáp án đúng:", "").strip()
            questions.append(question)  # Thêm câu hỏi sau khi đủ thông tin
    
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