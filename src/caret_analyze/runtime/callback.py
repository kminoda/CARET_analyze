# Copyright 2021 Research Institute of Systems Planning, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import List, Optional

from .path_base import PathBase
from .publisher import Publisher
from .subscription import Subscription
from .timer import Timer
from ..common import Summarizable, Summary
from ..infra.interface import RecordsProvider
from ..record import RecordsInterface
from ..value_objects import (CallbackType, CallbackStructValue,
                             SubscriptionCallbackStructValue,
                             TimerCallbackStructValue)


class CallbackBase(PathBase, Summarizable):
    """A base class that represents callback."""

    def __init__(
        self,
        info: CallbackStructValue,
        records_provider: RecordsProvider,
        subscription: Optional[Subscription],
        publishers: Optional[List[Publisher]],
        timer: Optional[Timer]
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        info : CallbackStructValue
            static info.
        records_provider : RecordsProvider
            provider to be evaluated.
        subscription : Optional[Subscription]
            None except for subscription callbacks.
        publishers : Optional[List[Publisher]]
            publishers to which the callback publishes.
        timer : Optional[Timer]
            None except for timer callbacks.

        """
        super().__init__()
        self.__val = info
        self._provider = records_provider
        self._sub = subscription
        self._pubs = publishers
        self._timer = timer

    @property
    def node_name(self) -> str:
        """
        Get node name.

        Returns
        -------
        str
            node name containing this callback.

        """
        return self.__val.node_name

    @property
    def symbol(self) -> str:
        """
        Get callback symbol name.

        Returns
        -------
        str
            callback function symbol name.

        """
        return self.__val.symbol

    @property
    def callback_name(self) -> str:
        """
        Get callback name defined in the architecture.

        Returns
        -------
        str
            callback name defined in architecture.

        """
        return self.__val.callback_name

    @property
    def callback_type(self) -> CallbackType:
        """
        Get callback type.

        Returns
        -------
        CallbackType
            callback type.

        """
        return self.__val.callback_type

    @property
    def subscription(self) -> Optional[Subscription]:
        """
        Get subscription.

        Returns
        -------
        Optional[Subscription]
            subscription which the callback is attached.
            None except for subscription callback.

        """
        return self._sub

    @property
    def publishers(self) -> Optional[List[Publisher]]:
        """
        Get publishers.

        Returns
        -------
        Optional[List[Publisher]]
            publishers to which the callback publishes.

        """
        if self._pubs is None:
            return None
        return sorted(self._pubs, key=lambda x: x.topic_name)

    @property
    def timer(self) -> Optional[Timer]:
        """
        Get timer.

        Returns
        -------
        Optional[Timer]
            timer which the callback is attached.
            None except for timer callback.

        """
        return self._timer

    @property
    def publish_topic_names(self) -> Optional[List[str]]:
        """
        Get publisher topic names.

        Returns
        -------
        Optional[List[str]]
            topic name list to be published by the callback.

        """
        if self.__val.publish_topic_names is None:
            return None
        return sorted(self.__val.publish_topic_names)

    @property
    def subscribe_topic_name(self) -> Optional[str]:
        """
        Get subscription topic name.

        Returns
        -------
        Optional[str]
            topic name to be subscribed by the callback.
            None except for subscription callback.

        """
        return self.__val.subscribe_topic_name

    @property
    def summary(self) -> Summary:
        """
        Get summary [override].

        Returns
        -------
        Summary
            summary info.

        """
        return self.__val.summary

    def _to_records_core(self) -> RecordsInterface:
        """
        Calculate records [override].

        Returns
        -------
        RecordsInterface
            callback duration (callback start - callback end).

        """
        records = self._provider.callback_records(self.__val)

        return records


class TimerCallback(CallbackBase):
    """Class that represents timer callback."""

    def __init__(
        self,
        callback: TimerCallbackStructValue,
        records_provider: RecordsProvider,
        publishers: Optional[List[Publisher]],
        timer: Timer
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        callback : TimerCallbackStructValue
            static info.
        records_provider : RecordsProvider
            provider to be evaluated.
        publishers : Optional[List[Publisher]]
            publishers to which the callback publishers
        timer : Timer
            timer

        """
        super().__init__(callback, records_provider, None, publishers, timer)
        self.__val: TimerCallbackStructValue = callback

    @property
    def period_ns(self) -> int:
        """
        Get timer period.

        Returns
        -------
        int
            timer period [ns].

        """
        return self.__val.period_ns


class SubscriptionCallback(CallbackBase):
    """A class that represents subscription callback."""

    def __init__(
        self,
        callback_info: SubscriptionCallbackStructValue,
        records_provider: RecordsProvider,
        subscription: Subscription,
        publishers: Optional[List[Publisher]] = None,
    ) -> None:
        """
        Constructor.

        Parameters
        ----------
        callback_info : SubscriptionCallbackStructValue
            static info.
        records_provider : RecordsProvider
            provider to be evaluated.
        subscription : Subscription
            subscription to which callback subscribes.
        publishers : Optional[List[Publisher]]
            publishers to which the callback publishers

        """
        super().__init__(callback_info, records_provider, subscription, publishers, None)
