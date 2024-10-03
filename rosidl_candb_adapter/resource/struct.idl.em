@{
from rosidl_candb_pycommon.utils import escape

from rosidl_candb_adapter import deduce_idl_type

struct_name = naming_convention.struct(message.name)
}@
@@verbatim(language="comment", text=
    "@(message.name)\n"
    "\n"
@[if message.comments]@
    "Comments:\n"
@[  for language, comment in message.comments.items()]@
    " - @(language ? f"{language}: ")@(escape(comment))\n"
@[  end for]@
    "\n"
    "Database: @(database_name)\n"
@[end if]@
    "Cycle Time: @(message.cycle_time ? f"{message.cycle_time} ms" ! "Event")\n"
@[if message.senders]@
    "Senders:\n"
@[  for node in message.senders]@
    " - @(node)\n"
@[  end for]@
@[end if]@
@[if message.receivers]@
    "Receivers:\n"
@[  for node in message.receivers]@
    " - @(node)\n"
@[  end for]@
@[end if]@
    "\n")
struct @(struct_name) {
@[if message.signals]@
@[  for signal in message.signals]@
@{      signal_idl_type = deduce_idl_type(signal)}@
    @@verbatim(language="comment", text=
        "@(signal.name)\n"
        "\n"
@[      if signal.comments]@
        "Comments:\n"
@[      for language, comment in signal.comments.items()]@
        " - @(language ? f"{language}: ")@(escape(comment))\n"
@[      end for]@
        "\n"
@[      end if]@
        "Range: @(signal.minimum)..@(signal.maximum)\n"
@[      if signal.unit]@
        "Unit: @(escape(signal.unit))\n"
@[      end if]@
        "\n")
    @(signal_idl_type) @(naming_convention.field(message.name, signal.name));

@[  end for]@
@[else]@
    uint8 structure_needs_at_least_one_member;
@[end if]@
};@
