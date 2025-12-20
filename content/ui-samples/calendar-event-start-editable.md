<Path>Add-ons > Calendar > Calendar with event drag and drop</Path>

To enable event drag-and-drop, set the eventStartEditable property to true. The EventDropEvent is fired when a calendar event is moved to another position. In this event, you can save an entity or persist any other information.

calendar-event-start-editable.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <data>
        <collection id="eventsDc" class="io.jmix.uisamples.entity.Event">
            <loader id="eventsDl">
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
        <div classNames="border rounded-s p-s">
            <span text="msg://sampleDescription.text"/>
        </div>
        <calendar:calendar id="calendar"
                           height="100%"
                           width="100%"
                           eventStartEditable="true"
                           minHeight="30em">
            <calendar:dataProviders>
                <calendar:containerDataProvider dataContainer="eventsDc"
                                                title="title"
                                                allDay="allDay"
                                                startDateTime="startDate"
                                                endDateTime="endDate"/>
            </calendar:dataProviders>
        </calendar:calendar>
    </layout>
</view>



CalendarEventStartEditableSample.java

package io.jmix.uisamples.view.flowui.calendar.eventstarteditable;

import com.vaadin.flow.component.notification.Notification;
import io.jmix.core.DataManager;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.fullcalendarflowui.component.data.EntityCalendarEvent;
import io.jmix.fullcalendarflowui.component.event.EventDropEvent;
import io.jmix.uisamples.entity.Event;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("calendar-event-start-editable")
@ViewDescriptor("calendar-event-start-editable.xml")
public class CalendarEventStartEditableSample extends StandardView {

    @Autowired
    private DataManager dataManager;
    @Autowired
    private Notifications notifications;

    @Subscribe("calendar")
    public void onCalendarEventDrop(final EventDropEvent event) {
        EntityCalendarEvent<Event> calendarEvent = event.getCalendarEvent();

        dataManager.save(calendarEvent.getEntity());

        notifications.create("Event: \"%s\" is saved".formatted(calendarEvent.getTitle()))
                .withType(Notifications.Type.SUCCESS)
                .withPosition(Notification.Position.TOP_END)
                .show();
    }
}




Event.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDateTime;
import java.util.UUID;

@JmixEntity
@Table(name = "EVENT")
@Entity
public class Event {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "TITLE")
    private String title;

    @Column(name = "START_DATE")
    private LocalDateTime startDate;

    @Column(name = "END_DATE")
    private LocalDateTime endDate;

    @Column(name = "ALL_DAY")
    private Boolean allDay;

    public Boolean getAllDay() {
        return allDay;
    }

    public void setAllDay(Boolean allDay) {
        this.allDay = allDay;
    }

    public LocalDateTime getEndDate() {
        return endDate;
    }

    public void setEndDate(LocalDateTime endDate) {
        this.endDate = endDate;
    }

    public LocalDateTime getStartDate() {
        return startDate;
    }

    public void setStartDate(LocalDateTime startDate) {
        this.startDate = startDate;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


