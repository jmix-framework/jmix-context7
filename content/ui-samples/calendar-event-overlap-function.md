<Path>Add-ons > Calendar > Calendar with event overlap function</Path>

This sample demonstrates how to add calendar event overlap rules. The overlap function takes two parameters: stillEvent - the overlapped event. movingEvent - the event that overlaps another one. Additional properties are placed in the extendedProps property. The property path will be formatted into a single property that joins properties with a capitalized first letter.

calendar-event-overlap-function.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <data>
        <collection id="backgroundEventsDc" class="io.jmix.uisamples.entity.BackgroundEvent">
            <fetchPlan extends="_base">
                <property name="workingShift" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="backgroundEventsDl" readOnly="true">
                <query>
                    <![CDATA[select e from BackgroundEvent e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <div classNames="rounded-panel">
            <span text="msg://sampleDescription.text"/>
        </div>
        <calendar:calendar id="calendar"
                           eventStartEditable="true"
                           eventDurationEditable="true"
                           eventResizableFromStart="true"
                           height="100%"
                           width="100%"
                           minHeight="30em">
            <calendar:dataProviders>
                <calendar:containerDataProvider dataContainer="backgroundEventsDc"
                                                title="title"
                                                allDay="allDay"
                                                display="display"
                                                startDateTime="startDate"
                                                endDateTime="endDate"
                                                classNames="classNames"
                                                additionalProperties="workingShift.number"/>
            </calendar:dataProviders>
        </calendar:calendar>
    </layout>
</view>



CalendarEventOverlapFunctionSample.java

package io.jmix.uisamples.view.flowui.calendar.eventoverlapfunction;

import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.CalendarEvent;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;
import io.jmix.fullcalendarflowui.kit.component.model.JsFunction;
import org.apache.groovy.util.Maps;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@ViewController("calendar-event-overlap-function")
@ViewDescriptor("calendar-event-overlap-function.xml")
public class CalendarEventOverlapFunctionSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Subscribe
    public void onInit(final InitEvent event) {
        calendar.setEventOverlapJsFunction(new JsFunction("""
                function(stillEvent, movingEvent) {
                    console.dir(stillEvent);
                    const stillEventProps = stillEvent.extendedProps;
                    const movingEventProps = movingEvent.extendedProps;
                    return stillEventProps.workingShiftNumber === movingEventProps.workingShiftNumber;
                }
                """));

        calendar.addDataProvider(new ListCalendarDataProvider(generateEvents()));
    }

    private List<CalendarEvent> generateEvents() {
        return List.of(
                SimpleCalendarEvent.create()
                        .withTitle("Event for WS #1")
                        .withAllDay(true)
                        .withStartDateTime(LocalDate.now().withDayOfMonth(10), LocalTime.MIDNIGHT)
                        .withEndDateTime(LocalDate.now().withDayOfMonth(12), LocalTime.MIDNIGHT)
                        .withAdditionalProperties(Maps.of("workingShiftNumber", "WS #1"))
                        .build(),
                SimpleCalendarEvent.create()
                        .withTitle("Event for WS #2")
                        .withAllDay(true)
                        .withStartDateTime(LocalDate.now().withDayOfMonth(13), LocalTime.MIDNIGHT)
                        .withEndDateTime(LocalDate.now().withDayOfMonth(15), LocalTime.MIDNIGHT)
                        .withAdditionalProperties(Maps.of("workingShiftNumber", "WS #2"))
                        .build()
        );
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




BackgroundEvent.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import io.jmix.fullcalendarflowui.component.model.Display;
import jakarta.annotation.Nullable;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
@Table(name = "BACKGROUND_EVENT", indexes = {
        @Index(name = "IDX_BACKGROUND_EVENT_WORKING_SHIFT", columnList = "WORKING_SHIFT_ID")
})
@Entity
public class BackgroundEvent {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "TITLE")
    private String title;

    @Column(name = "START_DATE")
    private LocalDate startDate;

    @Column(name = "END_DATE")
    private LocalDate endDate;

    @Column(name = "DISPLAY")
    private String display;

    @Column(name = "ALL_DAY")
    private Boolean allDay;

    @JoinColumn(name = "WORKING_SHIFT_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private WorkingShift workingShift;

    @Column(name = "CLASS_NAMES")
    private String classNames;

    public String getClassNames() {
        return classNames;
    }

    public void setClassNames(String classNames) {
        this.classNames = classNames;
    }

    public WorkingShift getWorkingShift() {
        return workingShift;
    }

    public void setWorkingShift(WorkingShift workingShift) {
        this.workingShift = workingShift;
    }

    public Boolean getAllDay() {
        return allDay;
    }

    public void setAllDay(Boolean allDay) {
        this.allDay = allDay;
    }

    @Nullable
    public Display getDisplay() {
        return display == null ? null : Display.fromId(display);
    }

    public void setDisplay(@Nullable Display display) {
        this.display = display == null ? null : display.getId();
    }

    public LocalDate getEndDate() {
        return endDate;
    }

    public void setEndDate(LocalDate endDate) {
        this.endDate = endDate;
    }

    public void setStartDate(LocalDate startDate) {
        this.startDate = startDate;
    }

    public LocalDate getStartDate() {
        return startDate;
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




WorkingShift.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "WORKING_SHIFT", indexes = {
        @Index(name = "IDX_WORKING_SHIFT_UNQ", columnList = "NUMBER_", unique = true)
})
@Entity
public class WorkingShift {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @NotNull
    @Column(name = "NUMBER_", nullable = false)
    private String number;

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




calendar-event-overlap-function.css

jmix-full-calendar .fc-event.green-background-event {
    background: var(--aura-green);
    border-radius: inherit;
    color: var(--aura-accent-contrast-color);
}

jmix-full-calendar .fc-event.red-background-event {
    background: var(--aura-red);
    border-radius: inherit;
    color: var(--aura-accent-contrast-color);
}


