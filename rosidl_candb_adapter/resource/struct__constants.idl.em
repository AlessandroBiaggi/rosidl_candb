@{
from rosidl_candb_pycommon.utils import message_constants

from rosidl_candb_adapter import deduce_idl_type
from rosidl_candb_adapter import format_idl_constant

constants = message_constants(message)
}@
module @(struct_name)_Constants {
    const uint32 @(naming_convention.id(struct_name)) = @(format_idl_constant(message.frame_id, 'uint32'));
    const uint32 @(naming_convention.length(struct_name)) = @(format_idl_constant(message.length, 'uint32'));
    const uint32 @(naming_convention.cycle_time(struct_name)) = @(format_idl_constant(message.cycle_time or 0, 'uint32'));
    const boolean @(naming_convention.is_fd(struct_name)) = @(format_idl_constant(message.is_fd, 'boolean'));
@[for signal, constant in constants.items()]@
@{  signal_idl_type = deduce_idl_type(signal) }@
    const @(signal_idl_type) @(naming_convention.scale(struct_name, signal.name)) = @(format_idl_constant(constant['scale'], signal_idl_type));
    const @(signal_idl_type) @(naming_convention.offset(struct_name, signal.name)) = @(format_idl_constant(constant['offset'], signal_idl_type));
@[  if 'initial' in constant]@
    @@verbatim(language="comment", text="@(signal.name) initial value")
    const @(signal_idl_type) @(naming_convention.initial(struct_name, signal.name)) = @(format_idl_constant(constant['initial'], signal_idl_type));
@[  end if]@
@[  if 'invalid' in constant]@
    @@verbatim(language="comment", text="@(signal.name) invalid value")
    const @(signal_idl_type) @(naming_convention.invalid(struct_name, signal.name)) = @(format_idl_constant(constant['invalid'], signal_idl_type));
@[  end if]@
@[  if 'choices' in constant]@
@{      unique_choices = dict() }@
@[      for choice_name, choices in constant['choices'].items()]@
@{          choice_name = naming_convention.choice(message.name, signal.name, choice_name) }@
@[          if choice_name not in unique_choices]@
@{              unique_choices[choice_name] = choices }@
@[          else]@
@{              unique_choices[choice_name].extend(choices) }@
@[          end if]@
@[      end for]@
@[      for choice_name, choices in unique_choices.items()]@
@[          if len(choices) == 1]@
    @@verbatim(language="comment", text="@(signal.name): '@(choices[0].name)' = @(choices[0].value)")
    const @(signal_idl_type) @(choice_name) = @(format_idl_constant(choices[0].value, signal_idl_type));
@[          else]@
@[              for choice in choices]@
    @@verbatim(language="comment", text="@(signal.name): @(choice.name) = @(choice.value)")
@{                  choice_value = format_idl_constant(choice.value, signal_idl_type) }@
    const @(signal_idl_type) @(choice_name)__@(choice_value) = @(choice_value);
@[              end for]@
@[          end if]@
@[      end for]@
@[  end if]@
@[end for]@
};@
