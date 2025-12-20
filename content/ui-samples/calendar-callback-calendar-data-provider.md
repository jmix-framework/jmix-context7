<Path>Add-ons > Calendar > Calendar with CallbackCalendarDataProvider</Path>

The CallbackCalendarDataProvider loads data only when the component needs new events. The calendar requires new data in the following cases: When the user switches to a calendar display mode that has a wider date range than the previous one. When FullCalendar's navigation methods are invoked (e.g. #navigateToNext()). When the time zone of the component is changed.

calendar-callback-calendar-data-provider.xml

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
                <calendar:callbackDataProvider title="title"
                                               allDay="allDay"
                                               startDateTime="startDate"
                                               endDateTime="endDate">
                    <calendar:itemsQuery class="io.jmix.uisamples.entity.Event"
                                         fetchPlan="_base">
                        <calendar:query>
                            <![CDATA[select e from Event e
                                        where e.startDate >= :fetchStartDate
                                            and e.endDate < :fetchEndDate]]>
                        </calendar:query>
                    </calendar:itemsQuery>
                </calendar:callbackDataProvider>
            </calendar:dataProviders>
        </calendar:calendar>
    </layout>
</view>



CalendarCallbackCalendarDataProviderSample.java

package io.jmix.uisamples.view.flowui.calendar.callbackcalendardataprovider;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;

@ViewController("calendar-callback-calendar-data-provider")
@ViewDescriptor("calendar-callback-calendar-data-provider.xml")
public class CalendarCallbackCalendarDataProviderSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Subscribe(id = "previousBtn", subject = "clickListener")
    public void onPreviousBtnClick(final ClickEvent<JmixButton> event) {
        calendar.navigateToPrevious();
    }

    @Subscribe(id = "nextBtn", subject = "clickListener")
    public void onNextBtnClick(final ClickEvent<JmixButton> event) {
        calendar.navigateToNext();
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


