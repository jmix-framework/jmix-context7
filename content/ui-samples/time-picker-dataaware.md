<Path>Components > TimePicker > Data-aware TimePicker</Path>

The dataContainer and property attributes are used to connect the TimePicker to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

time-picker-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="taskDc"
                  class="io.jmix.uisamples.entity.Task"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <timePicker id="timePicker" label="TimePicker"
                         dataContainer="taskDc" property="dueDate"/>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




TimePickerDataawareSample.java

package io.jmix.uisamples.view.flowui.components.timepicker.dataaware;

import com.vaadin.flow.component.html.Span;
import io.jmix.core.Metadata;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.timepicker.TypedTimePicker;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Task;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalTime;
import java.util.Date;
import java.util.TimeZone;

@ViewController("time-picker-dataaware")
@ViewDescriptor("time-picker-dataaware.xml")
public class TimePickerDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Task> taskDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    @Subscribe
    protected void onInit(InitEvent event) {
        Task task = metadata.create(Task.class);
        task.setDueDate(new Date());
        taskDc.setItem(task);
    }

    @Subscribe("timePicker")
    protected void onTimePickerValueChange(TypedValueChangeEvent<TypedTimePicker<Date>, Date> event) {
        LocalTime localTime = LocalTime.ofInstant(taskDc.getItem().getDueDate().toInstant(),
                TimeZone.getDefault().toZoneId());
        spanValue.setText(String.valueOf(localTime));
    }
}




Task.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.util.Date;
import java.util.UUID;

@Table(name = "TASK")
@Entity
@JmixEntity
public class Task {

    @Id
    @Column(name = "ID")
    @JmixGeneratedValue
    protected UUID id;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    protected String name;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "DUE_DATE")
    protected Date dueDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ASSIGNEE_ID")
    protected Customer assignee;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "PARENT_TASK_ID")
    protected Task parentTask;

    public Task() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setParentTask(Task parentTask) {
        this.parentTask = parentTask;
    }

    public Task getParentTask() {
        return parentTask;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setDueDate(Date dueDate) {
        this.dueDate = dueDate;
    }

    public Date getDueDate() {
        return dueDate;
    }

    public void setAssignee(Customer assignee) {
        this.assignee = assignee;
    }

    public Customer getAssignee() {
        return assignee;
    }
}


