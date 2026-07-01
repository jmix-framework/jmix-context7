<Path>Add-ons > Kanban > Kanban hierarchical columns</Path>

The Kanban board component supports hierarchical columns. To define a hierarchical column, simply add the column to an existing column. There are two column display modes: TABS - display columns by tabs COLUMNS - display all columns within a parent column When using the TABS mode, you can control the default selected column using the selected attribute. Note: hierarchical columns are not displayed if the Kanban board has swimlanes defined.

kanban-hierarchical-columns.xml

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
        <checkbox id="columnModeCheckbox" label="msg://columnModeCheckbox.label"/>
        <kanban:kanban id="kanban" dataContainer="kanbanTasksDc"
                       height="100%"
                       width="100%"
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
                <kanban:column dataField="testing" label="msg://kanban.column.testing">
                    <kanban:columns>
                        <kanban:column dataField="manual" label="msg://kanban.column.testing.manual"/>
                        <kanban:column dataField="auto" label="msg://kanban.column.testing.auto"/>
                    </kanban:columns>
                </kanban:column>
                <kanban:column dataField="done" label="msg://kanban.column.done"/>
            </kanban:columns>
        </kanban:kanban>
    </layout>
</view>




KanbanHierarchicalColumnsSample.java

package io.jmix.uisamples.view.flowui.kanban.hierarchicalcolumns;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.view.*;
import io.jmix.kanbanflowui.component.Kanban;
import io.jmix.kanbanflowui.kit.component.JmixKanban;
import io.jmix.uisamples.entity.KanbanTask;

@ViewController("kanban-hierarchical-columns")
@ViewDescriptor("kanban-hierarchical-columns.xml")
public class KanbanHierarchicalColumnsSample extends StandardView {

    @ViewComponent
    private Kanban<KanbanTask> kanban;

    @Subscribe("columnModeCheckbox")
    public void onColumnModeCheckboxValueChange(final ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        kanban.setHierarchyMode(event.getValue()
                ? JmixKanban.HierarchyMode.TABS
                : JmixKanban.HierarchyMode.COLUMNS);
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
import org.jspecify.annotations.Nullable;

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
import org.jspecify.annotations.Nullable;

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


