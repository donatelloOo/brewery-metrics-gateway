from typing import Dict, Type
from pydantic import BaseModel, field_validator, Field, model_validator

from model.utils import find_class


class Config(BaseModel):
    # ---------------------------
    # Classes
    # ---------------------------

    class GatewayConfig(BaseModel):
        host: str = "0.0.0.0"
        port: int = 8080

    class HandlerConfig(BaseModel):
        path: str
        class_name: str
        class_type: Type = None

        @model_validator(mode="after")
        def resolve_class_type(self):
            from model.handler import Handler
            if self.class_type is None:
                self.class_type = find_class('handlers', Handler, self.class_name)
            return self

    class ForwarderConfig(BaseModel):
        server_url: str
        class_name: str
        class_type: Type = None

        @model_validator(mode="after")
        def resolve_class_type(self):
            from model.forwarder import Forwarder
            if self.class_type is None:
                self.class_type = find_class('forwarders', Forwarder, self.class_name)
            return self

    # ---------------------------
    # Root
    # ---------------------------

    gateway: GatewayConfig
    handlers: Dict[str, HandlerConfig] = Field(default_factory=Dict[str, HandlerConfig])
    forwarders: Dict[str, ForwarderConfig] = Field(default_factory=Dict[str, ForwarderConfig])

    @field_validator("handlers", mode="before")
    def set_handler_defaults(cls, field_value: Dict[str, HandlerConfig]) -> Dict[str, HandlerConfig]:
        if not field_value:
            return {}  # never null
        # provide default class_name if known and not set
        _default_classes = {
            "brewCreator": "BrewCreatorHandler"
        }
        for key, config in field_value.items():
            default_class = _default_classes.get(key, None)
            if default_class and config and not config.get('class_name'):
                config['class_name'] = default_class
        return field_value

    @field_validator("forwarders", mode="before")
    def set_forwarder_defaults(cls, field_value: Dict[str, ForwarderConfig]) -> Dict[str, ForwarderConfig]:
        if not field_value:
            return {}  # never null
        # provide default class_name if known and not set
        _default_classes = {
            "grainfather": "GrainfatherForwarder",
            "littlebock": "LittlebockForwarder"
        }
        for key, config in field_value.items():
            default_class = _default_classes.get(key, None)
            if default_class and config and not config.get('class_name'):
                config['class_name'] = default_class
        return field_value
