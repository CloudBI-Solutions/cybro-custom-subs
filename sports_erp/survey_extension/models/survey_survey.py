from odoo import models, fields


class Survey(models.Model):
    _inherit = 'survey.survey'

    # is_diary = fields.Boolean()

    def _get_conditional_maps(self):
        # print("hhhaiiia")
        triggering_answer_by_question = {}
        triggered_questions_by_answer = {}
        for question in self.question_ids:

            triggering_answer_by_question[question] = question.is_conditional and question.triggering_answer_id

            if question.is_conditional:
                print('question_is', question)
                if question.triggering_answer_id in triggered_questions_by_answer:
                    triggered_questions_by_answer[question.triggering_answer_id] |= question
                else:
                    triggered_questions_by_answer[question.triggering_answer_id] = question
        return triggering_answer_by_question, triggered_questions_by_answer
