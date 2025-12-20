<Path>Add-ons > Calendar > Calendar with ContainerCalendarDataProvider</Path>

The containerDataProvider is a base way to bind the FullCalendar component with a CollectionContainer and display entities as events. It requires defining the property mappings from the entity to the CalendarEvent.

calendar-container-calendar-data-provider.xml

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



CalendarContainerCalendarDataProviderSample.java

package io.jmix.uisamples.view.flowui.calendar.containercalendardataprovider;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("calendar-container-calendar-data-provider")
@ViewDescriptor("calendar-container-calendar-data-provider.xml")
public class CalendarContainerCalendarDataProviderSample extends StandardView {
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


