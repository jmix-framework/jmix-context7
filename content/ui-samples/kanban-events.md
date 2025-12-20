<Path>Add-ons > Kanban > Kanban events</Path>

The Kanban board component has a certain set of events that are available for listening. To subscribe to them: you need to define a listener in the view controller declaratively, or add it using the corresponding method of the component. Some events may contain additional information about the context. For example, the TaskClick event contains information about the entity of the task associated with the card that was clicked.

kanban-events.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:kanban="http://jmix.io/schema/kanban/ui">
    <data readOnly="true">
        <collection id="kanbanTasksDc" class="io.jmix.uisamples.entity.KanbanTask">
            <fetchPlan extends="_base"/>
            <loader id="kanbanTasksDl" readOnly="true">
                <query>
                    <![CDATA[select e from KanbanTask e order by e.name asc]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox classNames="buttons-panel">
            <button id="showAllBtn" text="msg://showAllBtn.text" icon="CIRCLE"/>
            <button id="resetExecutedBtn" text="msg://resetExecutedBtn.text" icon="REFRESH"/>
        </hbox>
        <hbox width="100%" height="100%">
            <kanban:kanban id="kanban" dataContainer="kanbanTasksDc"
                           classNames="flex-grow"
                           columnActionsEnabled="true"
                           collapsible="true"
                           columnReorderingAllowed="true"
                           taskTagsVisible="true">
                <kanban:propertiesMapping id="id"
                                          status="status"
                                          text="name"
                                          color="color"
                                          tags="tags"/>
                <kanban:columns>
                    <kanban:column dataField="todo" label="msg://kanban.column.todo"/>
                    <kanban:column dataField="in_progress" label="msg://kanban.column.in_progress"/>
                    <kanban:column dataField="testing" label="msg://kanban.column.testing"/>
                    <kanban:column dataField="done" label="msg://kanban.column.done"/>
                </kanban:columns>
            </kanban:kanban>
            <checkboxGroup id="eventsCheckboxGroup" label="msg://eventsCheckboxGroup.label" themeNames="vertical"
                           readOnly="true" classNames="flex-grow"/>
        </hbox>
    </layout>
</view>




KanbanEventsSample.java

package io.jmix.uisamples.view.flowui.kanban.events;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.ComponentEvent;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.kanbanflowui.component.Kanban;
import io.jmix.kanbanflowui.kit.component.event.*;
import io.jmix.uisamples.entity.KanbanTask;
import org.apache.groovy.util.Maps;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.HashSet;
import java.util.Set;

@ViewController("kanban-events")
@ViewDescriptor("kanban-events.xml")
public class KanbanEventsSample extends StandardView {

    @SuppressWarnings("rawtypes")
    @ViewComponent
    private JmixCheckboxGroup<Class<? extends ComponentEvent>> eventsCheckboxGroup;
    @ViewComponent
    private Kanban<KanbanTask> kanban;

    @Autowired
    private Notifications notifications;

    @SuppressWarnings("rawtypes")
    private final Set<Class<? extends ComponentEvent>> firedEvents = new HashSet<>();

    @Subscribe
    public void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(eventsCheckboxGroup,
                Maps.of(
                        KanbanColumnClickEvent.class, "Column click",
                        KanbanColumnDoubleClickEvent.class, "Column double-click",
                        KanbanTaskClickEvent.class, "Task click",
                        KanbanTaskDoubleClickEvent.class, "Task double-click",
                        KanbanColumnCollapseEvent.class, "Column collapse",
                        KanbanColumnExpandEvent.class, "Column expand",
                        KanbanColumnReorderEvent.class, "Column reordered",
                        KanbanColumnShowEvent.class, "Column show",
                        KanbanColumnHideEvent.class, "Column hide",
                        KanbanDragStartEvent.class, "Drag start",
                        KanbanDragEndEvent.class, "Drag end"
                )
        );
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnClick(final KanbanColumnClickEvent event) {
        showNotification("Column clicked: " + event.getColumn().getLabel());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnDoubleClick(final KanbanColumnDoubleClickEvent event) {
        showNotification("Column double-clicked: " + event.getColumn().getLabel());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanTaskClick(final KanbanTaskClickEvent<KanbanTask> event) {
        showNotification("Task clicked: " + event.getItem().getName());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanTaskDoubleClick(final KanbanTaskDoubleClickEvent<KanbanTask> event) {
        showNotification("Task double-clicked: " + event.getItem().getName());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnCollapse(final KanbanColumnCollapseEvent event) {
        showNotification("Column collapsed: " + event.getColumn().getLabel());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnExpand(final KanbanColumnExpandEvent event) {
        showNotification("Column expanded: " + event.getColumn().getLabel());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnReorder(final KanbanColumnReorderEvent event) {
        showNotification("Column reordered: " + event.getColumn().getLabel() + ". New index: " + event.getNewIndex());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnShow(final KanbanColumnShowEvent event) {
        showNotification("Column showed: " + event.getColumn().getLabel());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanColumnHide(final KanbanColumnHideEvent event) {
        showNotification("Column hidden: " + event.getColumn().getLabel());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanDragEnd(final KanbanDragEndEvent<KanbanTask> event) {
        showNotification("Task dropped: " + event.getItem().getName());
        addExecuted(event.getClass());
    }

    @Subscribe("kanban")
    public void onKanbanKanbanDragStart(final KanbanDragStartEvent<KanbanTask> event) {
        showNotification("Task dragged: " + event.getItem().getName());
        addExecuted(event.getClass());
    }

    @Subscribe("showAllBtn")
    public void onShowAllBtnClick(final ClickEvent<JmixButton> event) {
        kanban.showAllColumns();
    }

    @Subscribe("resetExecutedBtn")
    public void onResetExecutedBtnClick(final ClickEvent<JmixButton> event) {
        firedEvents.clear();
        eventsCheckboxGroup.clear();
    }

    private void showNotification(String message) {
        notifications.create(message)
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @SuppressWarnings("rawtypes")
    private void addExecuted(Class<? extends ComponentEvent> eventClass) {
        firedEvents.add(eventClass);
        eventsCheckboxGroup.setValue(firedEvents);
    }
}




KanbanTask.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import org.springframework.lang.Nullable;

import java.time.LocalDate;
import java.util.UUID;

@Table(name = "KANBAN_TASK", indexes = {
        @Index(name = "IDX_KANBAN_TASK_ASSIGNEE", columnList = "ASSIGNEE_ID")
})
@Entity
@JmixEntity
public class KanbanTask {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "STATUS", nullable = false)
    @NotNull
    private String status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ASSIGNEE_ID")
    private KanbanUser assignee;

    @Column(name = "COLOR")
    private String color;

    @Max(100)
    @Min(0)
    @Column(name = "PROGRESS")
    private Integer progress;

    @Column(name = "PRIORITY")
    private String priority;

    @Column(name = "DUE_DATE")
    private LocalDate dueDate;

    @Column(name = "TAGS")
    private String tags;

    public Integer getProgress() {
        return progress;
    }

    public void setProgress(Integer progress) {
        this.progress = progress;
    }

    @Nullable
    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public KanbanUser getAssignee() {
        return assignee;
    }

    public void setAssignee(KanbanUser assignee) {
        this.assignee = assignee;
    }

    @Nullable
    public TaskPriority getPriority() {
        return priority == null ? null : TaskPriority.fromId(priority);
    }

    public void setPriority(@Nullable TaskPriority priority) {
        this.priority = priority == null ? null : priority.getId();
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    @Nullable
    public String getTags() {
        return tags;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Nullable
    public TaskStatus getStatus() {
        return status == null ? null : TaskStatus.fromId(status);
    }

    public void setStatus(TaskStatus status) {
        this.status = status.getId();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




TaskStatus.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.springframework.lang.Nullable;

public enum TaskStatus implements EnumClass<String> {

    TODO("todo"),
    IN_PROGRESS("in_progress"),
    TESTING("testing"),
    TESTING_MANUAL("manual"),
    TESTING_AUTO("auto"),
    DONE("done");

    private final String id;

    TaskStatus(String id) {
        this.id = id;
    }

    @Override
    public String getId() {
        return id;
    }

    @Nullable
    public static TaskStatus fromId(String id) {
        for (TaskStatus at : TaskStatus.values()) {
            if (at.getId().equals(id)) {
                return at;
            }
        }
        return null;
    }
}


