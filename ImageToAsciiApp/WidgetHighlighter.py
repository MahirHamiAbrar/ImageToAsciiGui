# error highlighting style sheet
highlightStyleSheet = """/*HIGHLIGHT STYLESHEET START*/
						  border-color: rgb(248, 28, 109);
						  background-color: rgba(248, 28, 109, 50);
						  selection-background-color: rgba(248, 28, 109, 250);
						  /*HIGHLIGHT STYLESHEET END*/"""

# error highlighting
def highlightWidget(widget, focus=True):
	global highlightStyleSheet
	# create a new style sheet without removing the previous one (if present)
	stylesheet = f"{widget.styleSheet()}\n{highlightStyleSheet}"
	# set the new style sheet to the widget
	widget.setStyleSheet(stylesheet)

	# set focus to the widget if permitted
	if focus:
		widget.setFocus(True)

# remove highlight error
def unhighlightWidget(widget, focus=False):
	global highlightStyleSheet
	# remove the highlighting style sheet only
	stylesheet = widget.styleSheet().replace(highlightStyleSheet, '')
	# set the new style sheet to the widget
	widget.setStyleSheet(stylesheet)

	# set focus to the widget if permitted
	if focus:
		widget.setFocus(True)
