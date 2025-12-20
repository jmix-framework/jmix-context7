<Path>Add-ons > Calendar > CalendarEvent actions</Path>

You can subscribe to a series of events that are fired when the user performs certain actions on a calendar event. In addition to the events in the sample, you can subscribe to: EventMouseEnterEvent - is fired when the user mouses over a calendar event. EventMouseLeaveEvent - is fired when the user mouses out of a calendar event.

calendar-event-actions.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <data>
        <collection id="eventsDc" class="io.jmix.uisamples.entity.Event">
            <loader id="eventsDl" readOnly="true">
                <query>
                    <![CDATA[select e from Event e]]>
                </query>
            </loader>
            <fetchPlan extends="_base"/>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <calendar:calendar id="calendar"
                           eventDurationEditable="true"
                           eventStartEditable="true"
                           eventResizableFromStart="true"
                           height="100%"
                           width="100%"
                           minHeight="30em">
            <calendar:dataProviders>
                <calendar:containerDataProvider dataContainer="eventsDc"
                                                title="title"
                                                startDateTime="startDate"
                                                endDateTime="endDate"
                                                allDay="allDay"/>
            </calendar:dataProviders>
        </calendar:calendar>
    </layout>
</view>



CalendarEventActionsSample.java

package io.jmix.uisamples.view.flowui.calendar.eventactions;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.fullcalendarflowui.component.event.EventClickEvent;
import io.jmix.fullcalendarflowui.component.event.EventDropEvent;
import io.jmix.fullcalendarflowui.component.event.EventResizeEvent;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("calendar-event-actions")
@ViewDescriptor("calendar-event-actions.xml")
public class CalendarEventActionsSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("calendar")
    public void onCalendarResizeEvent(final EventResizeEvent event) {
        notifications.create("EventResizeEvent", "Event " + event.getCalendarEvent().getTitle() + " is resized")
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("calendar")
    public void onCalendarDropEvent(final EventDropEvent event) {
        notifications.create("EventDropEvent", "Event " + event.getCalendarEvent().getTitle() + " is dropped")
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("calendar")
    public void onCalendarClickEvent(final EventClickEvent event) {
        notifications.create("EventClickEvent", "Event " + event.getCalendarEvent().getTitle() + " is clicked")
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }
}


