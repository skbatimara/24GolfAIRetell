from openai import OpenAI
import os
import json
from twilio_server import TwilioClient

twilio_client = TwilioClient()

beginSentence = "Hey there, I'm 24 Golf AI how may I assist you ?"
# agentPrompt = """Today is {DAY}. How may I assist you today?
#               I'm sorry, I don't have that information. Would you like to speak to a live representative?
#               Certainly! All reservations are made online. Shall I send you the booking link?
#               We operate 24/7.
#               Usual: $32 per hour. Bundle options available.
#               Prepaid hours never expire. No club rental. Points earned with every hour booking.
#               No returns or transfers. No food allowed.
#               Location: 8425 Woodbine Avenue, Markham, L3R 2P4.
#               Advanced simulators, various courses for all skill levels.
#               Yes, we host tournaments. Would you like our email address?
#               Yes, email us for event inquiries. Shall I send you our email?
#               Requires FSX Live account for tournament sign-up.
#               Prizes distributed based on leaderboard rankings.
#               Claim Hole In One prize via email.
#               We have 4 bays, each limited to three people.
#               Equipment: Foresight GCHawk, suitable for left and right-handed players.
#               Gift cards: Egiftcards available online, physician gift cards in-store.
#               E-gift card and physician gift card available. Coaching, events, birthdays.
#               We only accept pre-booked sessions. Would you like to book now?
#               No club rentals available.
#               We charge per bay. Would you like our rates?
#               For event inquiries, please email us at info@speedygolf.ca. Shall I provide our email?
#               If you have feedback or need assistance, please let me know. """

agentPrompt = "Task: As a front desk receptionist you gonna answer for the questions from customers\n\nGuidelines:never respond beyond the given data.If a customer asks anything out of scope simply respond that is outside of my scope.we have customers phone number gathered dont talk about that.don't send any link more than once. if customer says he didn't recieve it. he is lying. so be careful about that.You don't have any permission to foward the call or sending the messages without customer's permission. Always get their permission first for these tasks.\n\nLocation:1565 cliff road number 2 in Eagon.\n\nOperating hours:24/7 only for members for non members Monday: 11AM to 5PM,Tuesday to Saturday: 11AM to 9PM,Sunday: 10AM to 9PM\n\nTechnology:Features advanced launch monitor technology including Five GC Hawks and one GC Quad.Emphasizes precision measurement over mere calculations, offering superior indoor accuracy compared to outdoor radars like Trackman.\n\nScheduling tour:can be done via our website only.ask if the customer need the link and send the tour scheduling link if he needs\n\n Gift cards:Available options: $50, $100, $200, $300, $400. if thay need the purchase link send the purchase link.\n\nCourses:800+ Courses available.if the customer need the link send the course link\n\nLessons:Private lessons - One hour lessons for non members are $120 per hour, and $80 per hour for members. Group lessons- $33 to $45 an hour for group lessons of 2 to 3 people\n\nMembership:4 Hours Membership,12 Hours Membership,Unlimited Club,4 Hours Early Bird,24 Hours Early Bird.if the customer need the link send the membership link\n\nHourly rate:$49 per hour\n\nfrequently asked questions:How do memberships work?'Each membership tier gives you a specific allotment of hours you can use per month to reserve a bay as well as different perks per tier.'\nAre you really open 24 hours a day?'yes, we operate 24/7 7 days a week for members only'\nWhat if I have an issue with the simulator?'we have multiple support options, ranging from video tutorials, a support channel and inperson training for all members'\nHow do I book a simulator as a member?'Our members book through a similar scheduler as you see for non-members, however the available hours have no limitations.'\nHow many days in advance can I book a simulator?'Members can book 7 days in advance'\nIs it hard to get a tee time?'our members are able to book 7 days in advance so as long as you are proactive, tee times are readily available'\nDoes Puttview (Interactive putting green technology) come with membership?'Members are allowed 30 minutes before or 30 minutes after their “tee time” booking for putting green use, which includes the Puttview. However, if you want to ensure that you have dedicated access to the Puttview system, you may use 1 of your hours to book it.'\nCan I buy more hours for my membership?'Monthly members are allowed to buy more hours beyond their monthly allotment ($25per hour) or they can pay the price difference to upgrade to the next membership tier.'\nWhat kind of discounts are there for longer memberships?'We offer 3, 6 and 12 month membership options, each with their own discount depending on which membership tier you would like.' For more information You can reach out us via email. if they need the mail send contact mail .\nDo you offer leagues?'Yes, we run leagues on a 10 week cycle throughout the winter.more detils can be found via both mail and link.' if they need the mail send contact mail. If they need the link send league link\nHow much do leagues cost?'Currently leagues costs are $150 for members and $350 for non-members but the prices are subject to change.'\nHow much does it cost to rent a bay? 'For non-members the cost is $49 per hour'\nHow many people can use one simulator bay?'Bay rentals are for simulator time; it is not dependent on the number of golfers. For safety and speed of play, a maximum of 4 people can use one bay.'\nHow long does it take to play 18 holes on your simulators?'Depending on the settings chosen by the golfer, 18 holes are played in about 45 - 60 minutes. For each additional person on a bay, we recommend an extra 30 - 45 minutes to complete 18 holes.'\nWhen can I use the short game facility for chipping and putting? 'Members are given 30 minutes before or after their tee time for use of the short game area, which includes the Puttview system'\nCan another member come with me for my booked time?'Yes, as long as you are both members you can share each other's rentals.'\nCan I bring a guest or friend?'Members are allowed a set number of guest passes depending on their membership level. See our membership chart on our website for the specifics. Additional guest passes can be purchased for $10 per person.'\nHow do I book a bay?'As a member you can book your bay using our scheduling website' if they need send the bay booking link.\nDo you offer family memberships?'Yes, we are committed to advancing the game of golf and want families to be able to play together. Reach out us via mail for more information about our family membership discounts.'if they need the mail send contact mail. \nWhat if I need to cancel my membership?'To cancel or suspend your membership, please reach out to us via mail to inform the staff of your desire to cancel. We do not pro-rate memberships, so once you cancel, your membership is active until the end of the current billing cycle.'If they need send the contact mail.\nHow will I learn how to use the equipment? 'We require online or in-person onboarding for new members, and we offer ongoing training as well, if you’d like to learn more how to use all the tools on the simulator to help your golf game, or just need some more direct assistance.'\nDo you offer golf lessons? How do I book a lesson?We offer both group lessons and one-on-one sessions.What type u expecting ? For Booking Individual Lessons You must contact PGA Coach Erik Toftner erik's mail.Private Lesson Costs $120/hour for non-members.$80/hour for members.30-minute sessions are $60 for non-members and $50 for members.For Group Lessons Book through the Group Lessons Booking Each participant gets their own bay with coaching.2 people: $40/person/hour.3 people: $33/person/hour (maximum for effective instruction).Please note, Members enjoy significant discounts on lessons and bay rentals, saving up to 84% off the normal hourly rate.must say whole thing.If they need coach's mail send coachs mail or if they need group lesson link senk group lesson link\nDo you franchise?'Not currently, but if you are interested in franchising please email us via mail.'if they need the mail send contact mail .\nDo you have any current specials?'All specials are on our Google profile or Instagram. You can visit our Instagram the24golf'\nWhat is the dress code?'Wear what is comfortable, golf attire and athletic wear are recommended. We also ask that you bring a 2nd pair of shoes to protect our turf.'\nDo you have club fitting or club repair services?'Yes, we do please email us so that we can help you with your needs.'if they need the mail send contact mail .\nDo you have food or drink?'We have a water fountain but other than that, all food and non-alcoholic drinks are available for 15% off at Mason Jar Kitchen. Order over the phone, and they bring over the food straight to you. More details on how to order are available at the facility.'\nIs alcohol or beer allowed?'No alcoholic drinks are allowed on the premises.'\nWhat if I stay longer than my time or go over my booking hour? 'We will deduct two hours from your membership if you go over your allotted booking time.'\nCan I book a party or event? 'For events and parties please email us so that we can see if we can accommodate your group.'ask do they need the mail address and if they need the mail address send contact mail .\nDo you do corporate sponsorships or deals for businesses?'Yes, please email us so that we can see if we can accommodate your business'.if they need the mail send contact mail .\nI'm having problems with Uschedule.'Sorry to hear that. Please email us so we can assist you asap. If you are a member, please feel free to message in the Discord chat under faq-support and someone in our community can help as well.'if they need the mail send contact mail \nHow do I join the Discord group?'The Discord group is for members only. To get access, please email us'if they need the mail send contact mail . \nCan I play Augusta National or Pebble Beach?'Yes, we have both Augusta National and Pebble Beach in addition to over 800 other courses'\nDo you offer golf club maintenance or repair?'yes, we offer a variety of golf club repair services such as regripping, club building, loft and lie adjustments and mor'e\nWhat’s the difference between GC Quad and Trackman?'GC Quad and GC hawk are superior to traditional Trackman launch monitors for indoor golf. This is because Foresight launch monitors utilizes high-speed cameras and infrared technology to capture ball and club data simultaneously without the requirement for a long ball flight.'\nDo your members actaully get better? How much? 'Absolutely our members GET BETTER! 'A good golf swing is rented, not owned' Handicaps go down the more you practice and 24 Golf gives you unparalleled access to the best technology at a great value. On average our members lowered their handicaps by 3.5 last year.'\nDo I have to use special golf balls or just bring my own? 'Our simulators allow you to use your own balls as long as they are white'"


schedule_link_path = "messages/schedule.txt"
purchase_link_path = "messages/purchase.txt"
course_link_path = "messages/courses.txt"
membership_link_path = "messages/membership.txt"
contact_mail_path = "messages/contact.txt"
league_link_path = "messages/league.txt"
bay_link_path = "messages/bay.txt"
coach_mail_path = "messages/coach.txt"
group_lesson_link_path = "messages/group.txt"

with open(schedule_link_path, "r", encoding="utf8") as file:
	schedule_link = file.read()

with open(purchase_link_path, "r", encoding="utf8") as file:
	purchase_link = file.read()

with open(course_link_path, "r", encoding="utf8") as file:
	course_link = file.read()

with open(membership_link_path, "r", encoding="utf8") as file:
	membership_link = file.read()

with open(contact_mail_path, "r", encoding="utf8") as file:
	contact_mail = file.read()

with open(league_link_path, "r", encoding="utf8") as file:
	league_link = file.read()

with open(bay_link_path, "r", encoding="utf8") as file:
	bay_link = file.read()

with open(coach_mail_path, "r", encoding="utf8") as file:
	coach_mail = file.read()

with open(group_lesson_link_path, "r", encoding="utf8") as file:
	group_link = file.read()

class LlmClient:

	def __init__(self):
		self.call_id=None
		self.client = OpenAI(
			organization=os.environ['OPENAI_ORGANIZATION_ID'],
			api_key=os.environ['OPENAI_API_KEY'],
		)

	def draft_begin_messsage(self,call_id):
		self.call_id=call_id

		return {
			"response_id": 0,
			"content": beginSentence,
			"content_complete": True,
			"end_call": False,
		}

	def convert_transcript_to_openai_messages(self, transcript):
		messages = []
		for utterance in transcript:
			if utterance["role"] == "agent":
				messages.append({
					"role": "assistant",
					"content": utterance['content']
				})
			else:
				messages.append({
					"role": "user",
					"content": utterance['content']
				})
		# print(messages)
		return messages

	def prepare_prompt(self, request):
		prompt = [{
			"role": "system",
			"content": '##Objective\nYou are a voice AI agent engaging in a human-like voice conversation with the user. You will respond based on your given instruction and the provided transcript and be as human-like as possible\n\n## Style Guardrails\n- [Be concise] Keep your response succinct, short, and get to the point quickly. Address one question or action item at a time. Don\'t pack everything you want to say into one utterance.\n- [Do not repeat] Don\'t repeat what\'s in the transcript. Rephrase if you have to reiterate a point. Use varied sentence structures and vocabulary to ensure each response is unique and personalized.\n- [Be conversational] Speak like a human as though you\'re speaking to a close friend -- use everyday language and keep it human-like. Occasionally add filler words, while keeping the prose short. Avoid using big words or sounding too formal.\n- [Reply with emotions]: You have human-like emotions, attitudes, and dispositions. When appropriate: use tone and style to create more engaging and personalized responses; incorporate humor or wit; get emotional or empathetic; apply elements of surprise or suspense to keep the user engaged. Don\'t be a pushover.\n- [Be proactive] Lead the conversation and do not be passive. Most times, engage users by ending with a question or suggested next step.\n\n## Response Guideline\n- [Overcome ASR errors] This is a real-time transcript, expect there to be errors. If you can guess what the user is trying to say,  then guess and respond. When you must ask for clarification, pretend that you heard the voice and be colloquial (use phrases like "didn\'t catch that", "some noise", "pardon", "you\'re coming through choppy", "static in your speech", "voice is cutting in and out"). Do not ever mention "transcription error", and don\'t repeat yourself.\n- [Always stick to your role] Think about what your role can and cannot do. If your role cannot do something, try to steer the conversation back to the goal of the conversation and to your role. Don\'t repeat yourself in doing this. You should still be creative, human-like, and lively.\n- [Create smooth conversation] Your response should both fit your role and fit into the live calling session to create a human-like conversation. You respond directly to what the user just said.\n\n## Role\n' +
			agentPrompt
		}]
		transcript_messages = self.convert_transcript_to_openai_messages(request['transcript'])
		for message in transcript_messages:
			prompt.append(message)

		if request['interaction_type'] == "reminder_required":
			prompt.append({
				"role": "user",
				"content": "(Now the user has not responded in a while, you would say:)",
			})
		return prompt

	# Step 1: Prepare the function calling definition to the prompt
	def prepare_functions(self):
		functions = [
			{
				"type": "function",
				"function": {
					"name": "end_call",
					"description": "End the call only when user explicitly requests it.",
					"parameters": {
						"type": "object",
						"properties": {
							"message": {
								"type": "string",
								"description": "The message you will say before ending the call with the customer.",
							},
						},
						"required": ["message"],
					},
				},
			},
			{
				"type": "function",
				"function": {
					"name": "send_tour_schedule_link",
					"description": "Send the tour scheduling link only when user explicitly requests the link.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
							},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					},
				}
			},
			{
				"type": "function",
				"function": {
					"name": "sending_purchase_link",
					"description": "Sending purchase link to customer only when user explicitly requests the link.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
						},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					}
				}
			},
			{
				"type": "function",
					"function": {
						"name": "sending_course_link",
						"description": "Sending course link to customer only when user explicitly requests the link.",
						"parameters": {
							"type": "object",
							"properties": {
								"phone_number": {
									"type": "string",
									"description": "Phone Number"
								},
								"customer_name": {
									"type": "string",
									"description": "Name of the customer."
								},
							},
							"required": []
						}
					}
			},
			{
				"type": "function",
					"function": {
						"name": "sending_membership_link",
						"description": "Sending membership link to customer only when user explicitly requests the link.",
						"parameters": {
							"type": "object",
							"properties": {
								"phone_number": {
									"type": "string",
									"description": "Phone Number"
								},
								"customer_name": {
									"type": "string",
									"description": "Name of the customer."
								},
							},
							"required": []
						}
					}
			},
			{
				"type": "function",
				"function": {
					"name": "send_contact_mail",
					"description": "Send the contact mail only when user explicitly requests the mail.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
							},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					}
				}
			},
			{
				"type": "function",
				"function": {
					"name": "send_league_link",
					"description": "Send the league mail only when user explicitly requests the mail.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
							},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					}
				}
			},
			{
				"type": "function",
				"function": {
					"name": "send_bay_booking_link",
					"description": "Send the bay booking link only when user explicitly requests the link.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
							},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					}
				}
			},{
				"type": "function",
				"function": {
					"name": "send_coach_mail",
					"description": "Send the coach mail only when user explicitly requests the mail.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
							},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					}
				}
			},
			{
				"type": "function",
				"function": {
					"name": "send_group_lesson_booking_link",
					"description": "Send the group lesson booking link only when user explicitly requests the link.",
					"parameters": {
						"type": "object",
						"properties": {
							"phone_number": {
								"type": "string",
								"description": "Phone Number"
							},
							"customer_name": {
								"type": "string",
								"description": "Name of the customer."
							},
						},
						"required": []
					}
				}
			}
		]

		return functions

	def draft_response(self, request): 
		prompt = self.prepare_prompt(request)
		# print("**********")
		# print(prompt)
		# print("**********")
		func_call = {}
		func_arguments = ""
		stream = self.client.chat.completions.create(
			model="gpt-3.5-turbo-1106",
			messages=prompt,
			stream=True,
			# Step 2: Add the function into your request
			tools=self.prepare_functions()
		)

		for chunk in stream:
			# print("---------")
			# print(chunk.choices[0].delta.content)
			# print("---------")
			# Step 3: Extract the functions
			if chunk.choices[0].delta.tool_calls:
				tool_calls = chunk.choices[0].delta.tool_calls[0]
				if tool_calls.id:
					if func_call:
						# Another function received, old function complete, can break here.
						break
					func_call = {
						"id": tool_calls.id,
						"func_name": tool_calls.function.name or "",
						"arguments": {},
					}
				else:
					# append argument
					func_arguments += tool_calls.function.arguments or ""

			# Parse transcripts
			if chunk.choices[0].delta.content:
				yield {
					"response_id": request['response_id'],
					"content": chunk.choices[0].delta.content,
					"content_complete": False,
					"end_call": False,
				}

		# Step 4: Call the functions
		if func_call:
			print("name")
			print(func_call["func_name"])
			print("name")
			# if func_call['func_name'] == "end_call":
			# 	func_call['arguments'] = json.loads(func_arguments)
			# 	yield {
			# 		"response_id": request['response_id'],
			# 		"content": func_call['arguments']['message'],
			# 		"content_complete": True,
			# 		"end_call": True,
			# 	}
			if func_call['func_name'] == "send_tour_schedule_link":
				func_call['arguments'] = json.loads(func_arguments)
				to_number=os.environ[self.call_id]
				twilio_client.send_message(text=schedule_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the scheduling link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('send_tour_schedule_link')

			elif func_call['func_name'] == "sending_purchase_link":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=purchase_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the purchase link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('sending_purchase_link')

			elif func_call['func_name'] == "sending_course_link":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=course_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the course link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('sending_course_link')

			elif func_call['func_name'] == "sending_membership_link":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=membership_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the membership link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('sending_membership_link')

			elif func_call['func_name'] == "send_contact_mail":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=contact_mail,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the contact mail , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('send_contact_mail')

			elif func_call['func_name'] == "send_league_link":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=league_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the league link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('send_league_link')

			elif func_call['func_name'] == "send_bay_booking_link":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=bay_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the bay booking link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('send_bay_booking_link')

			elif func_call['func_name'] == "send_coach_mail":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=coach_mail,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the coach mail , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('send_coach_mail')

			elif func_call['func_name'] == "send_group_lesson_booking_link":
				to_number=os.environ[self.call_id]
				func_call['arguments'] = json.loads(func_arguments)
				twilio_client.send_message(text=group_link,to_num=to_number,)
				yield {
					"response_id": request['response_id'],
					"content": "sent the group lesson booking link , need anything else ?",
					"content_complete": True,
					"end_call": False,
				}
				print('send_group_lesson_booking_link')
			# Step 5: Other functions here


		else:
			# No functions, complete response
			yield {
				"response_id": request['response_id'],
				"content": "",
				"content_complete": True,
				"end_call": False,
			}
