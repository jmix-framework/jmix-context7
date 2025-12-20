<Path>Add-ons > Calendar > Calendar with CallbackCalendarDataProvider and load delegate</Path>

The callbackDataProvider supports setting a load delegate in cases where the XML definition is not suitable. The load delegate must return a list of CalendarEvents. Please note that if it returns a list of EntityCalendarEventss, the data provider should specify the property mappings.

calendar-callback-load-delegate.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <hbox>
            <button id="previousBtn" icon="ANGLE_LEFT"/>
            <button id="nextBtn" icon="ANGLE_RIGHT"/>
        </hbox>
        <calendar:calendar id="calendar"
                           height="100%"
                           width="100%"
                           minHeight="30em">
            <calendar:dataProviders>
                <calendar:callbackDataProvider id="simpleEventsDataProvider"/>
                <calendar:callbackDataProvider id="entityEventsDataProvider"
                                               title="title"
                                               allDay="allDay"
                                               startDateTime="startDate"
                                               endDateTime="endDate"/>
            </calendar:dataProviders>
        </calendar:calendar>
    </layout>
</view>



CalendarCallbackLoadDelegateSample.java

package io.jmix.uisamples.view.flowui.calendar.calendarcallbackloaddelegate;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.CalendarEvent;
import io.jmix.fullcalendarflowui.component.data.CallbackCalendarDataProvider.ItemsFetchContext;
import io.jmix.fullcalendarflowui.component.data.EntityCalendarDataProvider;
import io.jmix.fullcalendarflowui.component.data.EntityCalendarEvent;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;
import io.jmix.uisamples.bean.EventService;
import io.jmix.uisamples.entity.Event;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDateTime;
import java.util.List;

@ViewController("calendar-callback-load-delegate")
@ViewDescriptor("calendar-callback-load-delegate.xml")
public class CalendarCallbackLoadDelegateSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Autowired
    private EventService eventService;
    @Autowired
    private Notifications notifications;

    @Install(to = "calendar.simpleEventsDataProvider", subject = "loadDelegate")
    private List<CalendarEvent> calendarSimpleEventsDataProviderLoadDelegate(final ItemsFetchContext context) {
        return List.of(SimpleCalendarEvent.create()
                .withTitle("Simple event")
                .withStartDateTime(LocalDateTime.now())
                .build());
    }

    @Install(to = "calendar.entityEventsDataProvider", subject = "loadDelegate")
    private List<CalendarEvent> calendarEntityEventsDataProviderLoadDelegate(final ItemsFetchContext context) {
        showDataLoadingNotification();

        List<Event> events = eventService.fetchEvents(context.getStartDate(), context.getEndDate());

        return events.stream()
                .map(e -> (CalendarEvent) new EntityCalendarEvent<>(e,
                        (EntityCalendarDataProvider) context.getDataProvider()))
                .toList();
    }

    @Subscribe(id = "previousBtn", subject = "clickListener")
    public void onPreviousBtnClick(final ClickEvent<JmixButton> event) {
        calendar.navigateToPrevious();
    }

    @Subscribe(id = "nextBtn", subject = "clickListener")
    public void onNextBtnClick(final ClickEvent<JmixButton> event) {
        calendar.navigateToNext();
    }

    private void showDataLoadingNotification() {
        notifications.create("Loading events")
                .withPosition(Notification.Position.BOTTOM_END)
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




EventService.java

package io.jmix.uisamples.bean;

import io.jmix.core.DataManager;
import io.jmix.uisamples.entity.Event;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service("uisamples_EventService")
public class EventService {

    private final DataManager dataManager;

    public EventService(DataManager dataManager) {
        this.dataManager = dataManager;
    }

    public List<Event> fetchEvents(LocalDate start, LocalDate end) {
        return dataManager.load(Event.class)
                .query("select e from Event e where e.startDate >= :start and e.endDate < :end")
                .parameter("start", start.atStartOfDay())
                .parameter("end", end.atStartOfDay())
                .list();
    }
}


