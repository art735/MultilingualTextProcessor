from unittest import TestCase

import CommonTextIssuesRemover


class Test_CommonTextIssuesRemover(TestCase):

    def test_1(self):
        html_str = 'a      \n     b  \n\n\n\n\n\n    c'
        expected_result = 'a b c'
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = 'a <br>     <br> <br>   <br>    b  \n\n\n\n\n\n  <br><br><br><br><br><br>    c'
        expected_result = 'a<br><br>b<br><br>c'
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = '<br>     <br><br>   <br>x\ny    z<br>'
        expected_result = 'x y z'
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        # USE CASE "<br><br>- - -<br><br>"
        html_str = "abc- - -xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br><br>- - -<br><br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br>- - -xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br><br>- - -xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br><br><br>- - -xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc- - -<br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc- - -<br><br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc- - -<br><br><br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br>- - -<br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br><br>- - -<br><br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = "abc<br><br><br>- - -<br><br><br>xyz"
        expected_result = "abc<br><br>- - -<br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        # Тестировать случай: любое кол-во закрывающих тегов, стоящих между <br> и <br> должно встать перед первым <br>
        html_str = "abc<br></font></i><br>xyz"
        expected_result = "abc</font></i><br><br>xyz"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        # Между <br> и <br> не соблюдается условие, чтобы все теги были закрывающими, поэтому никаких перестановок
        # не будет, всё остаётся как есть
        html_str = "abc<br></font><b></i><br>xyz"
        expected_result = html_str
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        # Удалить подряд идущие открывающий и закрывающий теги с пустым содержимым между ними.
        html_str = r"<div></div>Some text <p></p>More text <a></a>"
        expected_result = "Some text More text"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        # Удалить пробелы между соседними открывающими тегами и между соседними закрывающими тегами
        html_str = r"<div> <span> <div> <span>"
        expected_result = r"<div><span><div><span>"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = r"</div> </span> </div> </span>"
        expected_result = r"</div></span></div></span>"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = r"<div> </span> <div> </span>"
        expected_result = r"<div> </span> <div> </span>"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = r"<div> <span> Text </div> </span> <b> </i> </b> <i> </p> </p>"
        expected_result = r"<div><span> Text </div></span> <b> </i></b> <i> </p></p>"
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)

        html_str = r'// англ. to mean'
        expected_result = r'// англ. to mean'
        actual_result = CommonTextIssuesRemover.fix_problems(html_str)
        self.assertEqual(expected_result, actual_result)
