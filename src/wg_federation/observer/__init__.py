"""
This package can ultimately be extracted from this program to act as an external library.

This package contains an EventDispatcher class in an event_dispatcher module.
EventDispatcher implements a full-featured observer pattern:

- `EventDispatcher` can register multiple `EventSubscriber` implementations.
`EventDispatcher` do not prevent the same `EventSubscriber` object to be registered twice or more.
This allows the same code to be run at different point in time.

- Any `EventSubscriber` implementation must advertise its order (default to `500`).
The `EventDispatcher` will run registered `EventSubscriber` implementations according to this order, lower values first.
When two `EventSubscriber` implementations or more share the same order value,
the order of registration is used to determine which will run first.
Because of the previous behavior, be careful in situation when you ignore the default order value. E.g:
    ```
    [...]
    event_dispatcher.register(subscriber1Order500()) # Run: 1st
    event_dispatcher.register(subscriber2Order500()) # Run: 2nd
    event_dispatcher.register(subscriber3Order500()) # Run: 3rd
    event_dispatcher.register(subscriberOrder501()) # Run: 4th (501 will always run after all 500)

    # Below is a better practice:

    [...]
    event_dispatcher.register(subscriber1Order500()) # Run: 1st
    event_dispatcher.register(subscriber2Order510()) # Run: 3rd
    event_dispatcher.register(subscriber3Order520()) # Run: 4th
    event_dispatcher.register(subscriberOrder501()) # Run: 2nd
    ```

- Any `EventSubscriber` implementation can stop the propagation of events after its run.
If set, this toggle will prevent any subsequent `EventSubscriber` to run, for any events.

- Any `EventSubscriber` implementation must advertise what events it listens to.
When `EventDispatcher` dispatches a list of events, if any events intersect with an `EventSubscriber`, it will run.

Examples:

#### An sandwich EventSubscriber that can run early and late

```
[...]

class Event(Enum):
    SANDWICH = 'sandwich'

class SandwichEventSubscriber(EventSubscriber):
    order: int = 1

    def __init__(self, order: int = 1);
        self.order = order

    def get_subscribed_events(self) -> list[Enum]:
        return [Event.SANDWICH]

    def run(self, data: BaseModel) -> Status:
        print('Running this sandwich event listener')
        return Status.SUCCESS

    def get_order(self) -> int:
        return self.order

early_subscriber = SandwichEventSubscriber()
late_subscriber = SandwichEventSubscriber(99999)
```
"""
