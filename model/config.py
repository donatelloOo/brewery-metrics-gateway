from typing import Dict, Type, Any
from pydantic import BaseModel, field_validator


class Config(BaseModel):
    # ---------------------------
    # Classes
    # ---------------------------

    class GatewayConfig(BaseModel):
        host: str = "0.0.0.0"
        port: int

    class HandlerConfig(BaseModel):
        path: str
        class_name: str
        # class_type: Type[Handler] = None

        # @field_validator("class_type", mode="before")
        # def resolve_class_type(cls, v: Type, values: dict[str, Any]) -> Type[Handler]:
        #    if not v:
        #        return gateway.find_class('handlers', Handler, values['class_name'])
        #    return v

    class ForwarderConfig(BaseModel):
        server_url: str
        class_name: str
        _class_type: Type

    # ---------------------------
    # Root
    # ---------------------------

    gateway: GatewayConfig
    handlers: Dict[str, HandlerConfig] = {}
    forwarders: Dict[str, ForwarderConfig] = {}

    @field_validator("handlers", mode="before")
    def set_handler_defaults(cls, handlers: Dict[str, HandlerConfig] | None) -> dict:
        if not handlers:
            return {}

        # provide default class_name if known and not set
        _default_handler_classes = {
            "brewCreator": "BrewCreatorHandler"
        }
        for key, config in handlers.items():
            default_class = _default_handler_classes.get(key, None)
            if default_class and config and not config.get('class_name', None):
                config['class_name'] = default_class

        return handlers

    @field_validator("forwarders", mode="before")
    def set_forwarder_defaults(cls, forwarders: Dict[str, ForwarderConfig] | None) -> dict:
        if not forwarders:
            return {}

        # provide default class_name if known and not set
        _default_forwarder_classes = {
            "grainfather": "GrainfatherForwarder",
            "littlebock": "LittlebockForwarder"
        }
        for key, config in forwarders.items():
            default_class = _default_forwarder_classes.get(key, None)
            if default_class and config and not config.get('class_name', None):
                config['class_name'] = default_class

        return forwarders
