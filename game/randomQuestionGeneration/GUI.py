from tkinter import *
from tkinter import messagebox as mb
from random import randrange
from randomQuestionGeneration.AngelaRQAI import AngelaRQAI
from audio_services.audio_sound_effect import AudioSoundEffect

question = []
options = []
answer = []

gameTitle = "AIQ Test"

_RQAI=AngelaRQAI()

class Quiz:
	def __init__(self):
		self.q_no=0
		self.opt_selected=IntVar()
		
		# Title
		Label(gui, text=gameTitle, width=62, bg="blue",fg="white", font=("ariel", 20, "bold")).place(x=0, y=2)

		self.display_question()
		
		self.opts=self.radio_buttons()

		self.display_options()
		self.buttons()
		
		self.data_size=len(question)
		self.correct=0


	def display_score(self):
		wrong_count = self.data_size - self.correct
		correct = f"Correct: {self.correct}"
		wrong = f"Wrong: {wrong_count}"

		score = int(self.correct / self.data_size * 100)
		result = f"Score: {score}%"

		play = AudioSoundEffect()
		if score >= 70:
			play.playSound(2)
		else:
			play.playSound(1)

		mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")


	def check_ans(self, q_no):
		
		if self.opt_selected.get() == (answer[q_no] + 1):
			return True


	def next_btn(self):
		
		if self.check_ans(self.q_no):
			self.correct += 1
		
		self.q_no += 1
		
		if self.q_no==self.data_size:
			self.display_score()
			gui.destroy()
		else:
			self.display_question()
			self.display_options()


	def buttons(self):		
		next_button = Button(gui, text="Next",command=self.next_btn,
		width=10,bg="blue",fg="blue",font=("ariel",16,"bold"))
		
		next_button.place(x=350,y=380)
		
		quit_button = Button(gui, text="Quit", command=gui.destroy,
		width=5,bg="black", fg="red",font=("ariel",16," bold"))
		
		quit_button.place(x=700,y=50)


	def display_options(self):
		val=0
		self.opt_selected.set(0)
		
		for option in options[self.q_no]:
			self.opts[val]['text']=option
			val+=1


	def display_question(self):
		text= Text(gui,wrap=WORD)
		q_no = Label(gui, text=question[self.q_no], width=60, wraplength=700, justify="left",
		font=( 'ariel' ,16, 'bold' ), anchor= 'w')
		
		q_no.place(x=70, y=90)


	def radio_buttons(self):
		q_list = []
		y_pos = 150
		
		while len(q_list) < 4:
			radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected,
			value = len(q_list)+1,font = ("ariel",14))
			
			q_list.append(radio_btn)
			radio_btn.place(x = 100, y = y_pos)			
			y_pos += 40

		return q_list


gui = Tk()
gui.geometry("800x450")
gui.title(gameTitle)

numberOfQuestions = 0
while numberOfQuestions < 10:
	dictionary = _RQAI.GetRandomQuestionAndAnswers("History")
	question.append(list(dictionary.keys())[0])

	# Randomly place answer in list (Swap)
	questionOptions = list(dictionary.values())
	num = randrange(4)
	qAnswer = questionOptions[0]
	questionOptions[0] = questionOptions[num]
	questionOptions[num] = qAnswer

	options.append(questionOptions)
	answer.append(num)
	numberOfQuestions += 1

quiz = Quiz()
gui.mainloop()
