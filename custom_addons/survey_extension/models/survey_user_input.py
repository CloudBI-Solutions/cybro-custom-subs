from odoo import models, fields, api
from odoo.tools.translate import _
from logging import getLogger


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.model
    def create(self, vals):
        """create methode"""
        # print("create\n", vals)
        result = super(SurveyUserInput, self).create(vals)
        return result

    def save_lines(self, question, answer, comment=None):
        # print("SAVE LINES---->", self, question, answer)
        """ Save answers to questions, depending on question type

            If an answer already exists for question and user_input_id, it will be
            overwritten (or deleted for 'choice' questions) (in order to maintain data consistency).
        """
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])
        if question.question_type in ['char_box', 'text_box', 'numerical_box', 'date', 'datetime']:
            self._save_line_simple_answer(question, old_answers, answer)
            if question.save_as_email and answer:
                self.write({'email': answer})
            if question.save_as_nickname and answer:
                self.write({'nickname': answer})

        elif question.question_type in ['simple_choice', 'multiple_choice']:
            self._save_line_choice(question, old_answers, answer, comment)
        elif question.question_type == 'matrix':
            self._save_line_matrix(question, old_answers, answer, comment)
        elif question.question_type == 'body_map':
            pass
        elif question.question_type == 'toggle':
            print("QUESTIONNN", question)
            print("ANSWERRRR", answer)
            real_answer = None
            if self.survey_id.questions_layout == 'page_per_section':
                if answer:
                    real_answer = 'Yes'
                elif not answer:
                    real_answer = 'No'
                print("real answer", real_answer)
                answer_ques = self.env['survey.question.answer'].search([
                    ('question_id', '=', question.id),
                    ('value', '=', real_answer)], limit=1)
                print('answerrrrrrrrr', answer_ques)
                answer = answer_ques
            self._save_line_toggle(question, old_answers, answer, comment)

        elif question.question_type == 'progress_bar':
            # print("progress_bar", question, old_answers, answer)
            self._save_line_progress_bar(question, old_answers, answer, comment)
        elif question.question_type == 'calculated_metric':
            self._save_line_calculated_metric(question, old_answers, answer, comment)
        elif question.question_type == 'file':
            self._save_line_file(question, old_answers, answer)
        else:
            raise AttributeError(question.question_type + ": This type of question has no saving function")

    def _save_line_file(self, question, old_answers, answer):
        vals = self._get_line_answer_values(question, answer, question.question_type)
        # print(">>>>>>>>>>>>>>",vals)
        if vals.get('value_file'):
            files_vals = vals.get('value_file').rsplit(',', 1)
            vals.update({'value_file':files_vals[1],'file_name':files_vals[0]})
            if vals.get('answer_type'):
                if old_answers:
                    old_answers.write(vals)
                    return old_answers
                else:
                    return self.env['survey.user_input.line'].create(vals)

    def _save_line_toggle(self, question, old_answers, answers, comment):
        print('___AAANNANSS', answers)
        print('QUESTTTTTT', question)
        if answers:
            self.write({'user_input_line_ids': [
                (0, 0, {'question_id': question.id, 'answer_type': 'toggle', 'value_toggle': True,
                        'suggested_answer_id': int(answers),
                        'toggle_answer': question.toggle_on_name})]})
        else:
            self.write({'user_input_line_ids': [
                (0, 0, {'question_id': question.id, 'answer_type': 'toggle', 'value_toggle': False,
                        'toggle_answer': question.toggle_off_name})]})

    def _save_line_progress_bar(self, question, old_answers, answers, comment):
        self.write({'user_input_line_ids': [
            (0, 0, {'question_id': question.id, 'answer_type': 'progress_bar',
                    'value_progress_bar': answers if answers else '0'})]})
        # print(self, self.user_input_line_ids)
        # for line in self.user_input_line_ids:
        #     print("type-->", line.answer_type, "\nans--->", line.value_progress_bar)

    def _save_line_calculated_metric(self, question, old_answers, answers, comment):
        self.write({'user_input_line_ids': [
            (0, 0, {'question_id': question.id, 'answer_type': 'calculated_metric',
                    'value_calculated_metric': answers if answers else '0'})]})

    def answer_prettify(self):
        res = {}
        for que in self.survey_id.question_and_page_ids:
            res.setdefault(que, [])
            for line in self.user_input_line_ids:

                if line.question_id.id == que.id:
                    if line.suggested_answer_id:
                        res[line.question_id].append(line.suggested_answer_id.value)
                    elif line.value_char_box:
                        res[line.question_id].append(line.value_char_box)
                    elif line.value_numerical_box:
                        res[line.question_id].append(line.value_numerical_box)
                    elif line.value_date:
                        res[line.question_id].append(line.value_date)
                    elif line.value_datetime:
                        res[line.question_id].append(line.value_datetime)
                    elif line.value_text_box:
                        res[line.question_id].append(line.value_text_box)
                    elif line.value_toggle:
                        res[line.question_id].append(line.value_toggle)
                    elif line.value_progress_bar:
                        res[line.question_id].append(line.value_progress_bar)
                    elif line.value_calculated_metric:
                        res[line.question_id]=[]

                        res[line.question_id].append(line.value_calculated_metric)
                    elif line.value_body_map:
                        list_string = []
                        for value in line.value_body_map:
                            line_string = ''
                            if value.pain_level:
                                line_string = 'Pain Level['+str(value.pain_level)+']'
                            if value.comment:
                                line_string += ' (' + value.comment + ')'
                            list_string.append(line_string)
                        res[line.question_id] = list_string
        return res

    def check_work(self):
        # print("hahahahahahhahaha")
        # print("vals", self)
        answer_id = self.id
        # print("answer", answer_id)
        question = self.env['survey.question'].search([
            ('triggering_answer_id', '=', answer_id)
        ])
        return question.id





        # for line in self.user_input_line_ids:
        #     res.setdefault(line.question_id, [])
        #     if line.suggested_answer_id:
        #         res[line.question_id].append(line.suggested_answer_id.value)
        #     elif line.value_char_box:
        #         res[line.question_id].append(line.value_char_box)
        #     elif line.value_numerical_box:
        #         res[line.question_id].append(line.value_numerical_box)
        #     elif line.value_date:
        #         res[line.question_id].append(line.value_date)
        #     elif line.value_datetime:
        #         res[line.question_id].append(line.value_datetime)
        #     elif line.value_text_box:
        #         res[line.question_id].append(line.value_text_box)
        #     elif line.value_toggle:
        #         res[line.question_id].append(line.value_toggle)
        #     elif line.value_progress_bar:
        #         res[line.question_id].append(line.value_progress_bar)
        #     elif line.value_calculated_metric:
        #         res[line.question_id].append(line.value_calculated_metric)
        #     elif line.value_body_map:
        #         list_string = []
        #         for value in line.value_body_map:
        #             line_string = ''
        #             if value.pain_level:
        #                 line_string = value.pain_level
        #             line_string += ' ' + value.comment
        #             list_string.append(line_string)
        #         res[line.question_id] = list_string
        # print(res)
        # return res

    def _clear_inactive_conditional_answers(self):
        """
        Clean eventual answers on conditional questions that should not have been displayed to user.
        This method is used mainly for page per question survey, a similar method does the same treatment
        at client side for the other survey layouts.
        E.g.: if depending answer was uncheck after answering conditional question, we need to clear answers
              of that conditional question, for two reasons:
              - ensure correct scoring
              - if the selected answer triggers another question later in the survey, if the answer is not cleared,
                a question that should not be displayed to the user will be.

        TODO DBE: Maybe this can be the only cleaning method, even for section_per_page or one_page where
        conditional questions are, for now, cleared in JS directly. But this can be annoying if user typed a long
        answer, changed his mind unchecking depending answer and changed again his mind by rechecking the depending
        answer -> For now, the long answer will be lost. If we use this as the master cleaning method,
        long answer will be cleared only during submit.
        """
        inactive_questions = self._get_inactive_conditional_questions()
        # inactive_questions = self
        # print("SELF", self)
        # print("inactive_questions", inactive_questions)
        inactive_questions_ids = []
        for ans in self.user_input_line_ids:
            print(ans.question_id)
        for inactive_question in inactive_questions:
            inactive_questions_ids.append(inactive_question.id)
            print("INACTIVE QS IDS---------------->", inactive_questions_ids)
            if inactive_question.is_conditional:
                print("QS TYPE", inactive_question.triggering_question_id)
                if inactive_question.triggering_question_id.question_type == "toggle":
                    print('inactive_ques', inactive_question.triggering_question_id)
                    user_input = self.env[
                        'survey.user_input.line'].sudo().search([
                        ('id', 'in',
                         self.user_input_line_ids.ids),
                        ('question_id', '=',
                         inactive_question.triggering_question_id.id)
                    ])
                    # print("user_input", user_input)
                    # print("VALUE TOGGLE--->", user_input.value_toggle)
                    print("inactive_question.triggering_answer_id.value", inactive_question)
                    for rec_input in user_input:
                        print('rec_input', rec_input)
                        if rec_input.value_toggle and inactive_question.triggering_answer_id.value == "Yes":
                            print("YES!!!!!!!!!!!!", rec_input.value_toggle)
                            print('inactive_questions_ids',
                                  inactive_questions_ids)
                            print("inactive_question", inactive_question.id)
                            if inactive_question.id in inactive_questions_ids:
                                inactive_questions_ids.remove(
                                    inactive_question.id)
                    # for ans in self.user_input_line_ids:
                    #     if ans.triggering_question_id =
                    # print("EXP ANS",
                    #       type(inactive_question.triggering_answer_id.value))
                    # user_ans = self.user_input_line_ids.filtered(lambda answer: answer.question_id == inactive_question)
                    # if inactive_question.triggering_answer_id.value == "Yes":
                    #     print("inactive_question----->", inactive_question)
                    # print("USER ANS", ans.toggle_answer)
                    # print(inactive_question.triggering_answer_id.value)
        # delete user.input.line on question that should not be answered.
        print("INACTIVE QS IDS Final---------------->", inactive_questions_ids)
        inactive_questions = self.env['survey.question'].sudo().search([
            ('id', 'in', inactive_questions_ids)
        ])
        print('inactive questions', inactive_questions)
        answers_to_delete = self.user_input_line_ids.filtered(
            lambda answer: answer.question_id in inactive_questions)
        answers_to_delete.unlink()

    def _get_conditional_values(self):
        print("BLAAAAAA")
        """ For survey containing conditional questions, we need a triggered_questions_by_answer map that contains
                {key: answer, value: the question that the answer triggers, if selected},
         The idea is to be able to verify, on every answer check, if this answer is triggering the display
         of another question.
         If answer is not in the conditional map:
            - nothing happens.
         If the answer is in the conditional map:
            - If we are in ONE PAGE survey : (handled at CLIENT side)
                -> display immediately the depending question
            - If we are in PAGE PER SECTION : (handled at CLIENT side)
                - If related question is on the same page :
                    -> display immediately the depending question
                - If the related question is not on the same page :
                    -> keep the answers in memory and check at next page load if the depending question is in there and
                       display it, if so.
            - If we are in PAGE PER QUESTION : (handled at SERVER side)
                -> During submit, determine which is the next question to display getting the next question
                   that is the next in sequence and that is either not triggered by another question's answer, or that
                   is triggered by an already selected answer.
         To do all this, we need to return:
            - list of all selected answers: [answer_id1, answer_id2, ...] (for survey reloading, otherwise, this list is
              updated at client side)
            - triggered_questions_by_answer: dict -> for a given answer, list of questions triggered by this answer;
                Used mainly for dynamic show/hide behaviour at client side
            - triggering_answer_by_question: dict -> for a given question, the answer that triggers it
                Used mainly to ease template rendering
        """
        triggering_answer_by_question, triggered_questions_by_answer = {}, {}
        # Ignore conditional configuration if randomised questions selection
        if self.survey_id.questions_selection != 'random':
            triggering_answer_by_question, triggered_questions_by_answer = self.survey_id._get_conditional_maps()
        # change the selected answer
        selected_answers = self._get_selected_suggested_answers()

        return triggering_answer_by_question, triggered_questions_by_answer, selected_answers

    def _get_selected_suggested_answers(self):
        print("haiiiiaia")
        """
        For now, only simple and multiple choices question type are handled by the conditional questions feature.
        Mapping all the suggested answers selected by the user will also include answers from matrix question type,
        Those ones won't be used.
        Maybe someday, conditional questions feature will be extended to work with matrix question.
        :return: all the suggested answer selected by the user.
        """

        # STATE CHANGED TO DONE !!!!!!!!!!!!
        # for rec in self:
        #     print('recc', rec)
        # print(self.survey_id)
        # print('ctx', self.search_read)
        print('sellfff', self)
        return self.mapped('user_input_line_ids.suggested_answer_id')
