w20e.forms: submission

In most cases a form needs to be submitted. This is not necessarily the same
as HTML form submission though. In a web situation, the form will be displayed
as HTML, and upon HTML submission the form will be handled on the backend.
Here we'll find the w20e.forms submission process. Submission is the process
of actually handling the data.

There's several submission handlers defined in this package, but if
you'd like your own, follow the steps:

1. create your submission handler according to the ISubmission interface defined
   in interfaces.py
2. register the handler with a unique id with the w20e.forms registry like so:

  from w20e.forms.registry import Registry

  Registry.register_submission('your_id', YourStorage)

What the package offers is:

	attr	Store the data in a single attribute on some context
	attrs	Store the data in a separate attributes, one per variable,
                on some context
	none	Do nothing...

