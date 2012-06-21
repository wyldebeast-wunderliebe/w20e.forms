""" Register renderers """

from w20e.forms.registry import Registry
from select import SelectRenderer
from checkbox import CheckboxRenderer
from input import InputRenderer
from password import PasswordRenderer
from hidden import HiddenRenderer
from text import TextRenderer
from cardgroup import CardGroupRenderer
from flowgroup import FlowGroupRenderer
from stepgroup import StepGroupRenderer
from submit import SubmitRenderer
from cancel import CancelRenderer
from richtext import RichTextRenderer
from file import FileRenderer


Registry.register_renderer("submit", "html", SubmitRenderer)
Registry.register_renderer("cancel", "html", CancelRenderer)
Registry.register_renderer("text", "html", TextRenderer)
Registry.register_renderer("input", "html", InputRenderer)
Registry.register_renderer("password", "html", PasswordRenderer)
Registry.register_renderer("hidden", "html", HiddenRenderer)
Registry.register_renderer("file", "html", FileRenderer)
Registry.register_renderer("checkbox", "html", CheckboxRenderer)
Registry.register_renderer("richtext", "html", RichTextRenderer)
Registry.register_renderer("select", "html", SelectRenderer)
Registry.register_renderer("range", "html", SelectRenderer)
Registry.register_renderer("flowgroup", "html", FlowGroupRenderer)
Registry.register_renderer("cardgroup", "html", CardGroupRenderer)
Registry.register_renderer("stepgroup", "html", StepGroupRenderer)
