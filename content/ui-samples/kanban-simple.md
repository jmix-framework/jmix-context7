<Path>Add-ons > Kanban > Simple Kanban</Path>

The Kanban board is designed to visually display work at various stages of a process using cards to represent tasks, and columns to represent each stage of the process. The component is based on the Smart HTML Elements - Kanban web-component. Since the component is used to visualize a set of entities, its functionality is somewhat similar to the DataGrid component. For example, the component can contain actions for creating, editing, and deleting entities. In addition, the component implements data binding. You can filter data using the GenericFilter component. All changes to the data set will be displayed on the Kanban board.

kanban-simple.xml

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
        <genericFilter dataLoader="kanbanTasksDl"/>
        <hbox classNames="buttons-panel">
            <button id="createBtn" action="kanban.create"/>
            <button id="editBtn" action="kanban.edit"/>
            <button id="removeBtn" action="kanban.remove"/>
        </hbox>
        <kanban:kanban id="kanban" dataContainer="kanbanTasksDc"
                       width="100%" height="100%">
            <kanban:propertiesMapping id="id" status="status" text="name"/>

            <kanban:actions>
                <kanban:action id="create" type="list_create">
                    <kanban:properties>
                        <kanban:property name="openMode" value="DIALOG"/>
                    </kanban:properties>
                </kanban:action>
                <kanban:action id="edit" type="list_edit">
                    <kanban:properties>
                        <kanban:property name="openMode" value="DIALOG"/>
                    </kanban:properties>
                </kanban:action>
                <kanban:action id="remove" type="list_remove"/>
            </kanban:actions>

            <kanban:columns>
                <kanban:column dataField="todo" label="msg://kanban.column.todo"/>
                <kanban:column dataField="in_progress" label="msg://kanban.column.in_progress"/>
                <kanban:column dataField="testing" label="msg://kanban.column.testing"/>
                <kanban:column dataField="done" label="msg://kanban.column.done"/>
            </kanban:columns>
        </kanban:kanban>
    </layout>
</view>




KanbanSimpleSample.java

package io.jmix.uisamples.view.flowui.kanban.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("kanban-simple")
@ViewDescriptor("kanban-simple.xml")
public class KanbanSimpleSample extends StandardView {
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


