""" Program configuration """
__author__ = "Rolf Johansson"
__description__ = "QTI converter utility"
__license__ = "Apache License 2.0"
__version__ = "0.1.0"

# String in img href to remove from XML
img_href_ims_base = "%24IMS-CC-FILEBASE%24/"

# Character to replace [blanks] in questions with
blanks_replace_str = "_"

# Number of replace characters in question text
blanks_question_n = 10

# Number of characters in answer line template
blanks_answer_n = 80

# Random shuffle of answers in type "Matching Question"
matching_random_shuffle_answers = True
matching_random_shuffle_answer_options = True

# If True, replace first set of variables in question text instead of displaying options
calculated_display_var_set_in_text = False
