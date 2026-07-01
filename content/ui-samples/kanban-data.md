<Path>Add-ons > Kanban > Kanban with data</Path>

The Kanban board component has the ability to bind data. To do this, specify the dataContainer attribute. You can filter and edit data in the container, all changes will be displayed in the component. To set the mapping of the attributes of the displayed entity with the attributes of the Kanban task card, you need to define the propertiesMapping object. The Kanban task card has the following set of attributes: id (required) status (required) text (required) username userAvatar color dueDate progress tags priority swimlane The rules for displaying matching elements to Kanban task cards can be controlled using the component properties. Required attributes have default values. If the propertiesMapping object is not specified, the entity will use the id, status, and text fields to determine the mapping.

kanban-data.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:kanban="http://jmix.io/schema/kanban/ui">
    <data>
        <collection id="kanbanTasksDc" class="io.jmix.uisamples.entity.KanbanTask">
            <fetchPlan extends="_base"/>
            <loader id="kanbanTasksDl">
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
        <hbox width="100%" wrap="true">
            <button id="createBtn" action="kanban.create"/>
            <button id="editBtn" action="kanban.edit"/>
            <button id="removeBtn" action="kanban.remove"/>
        </hbox>
        <kanban:kanban id="kanban" dataContainer="kanbanTasksDc"
                       width="100%"
                       height="100%"
                       taskDueDateVisible="true"
                       taskPriorityVisible="true"
                       taskUserAvatarVisible="true"
                       taskProgressVisible="true"
                       taskTagsVisible="true">
            <kanban:propertiesMapping id="id"
                                      status="status"
                                      text="name"
                                      username="assignee.name"
                                      userAvatar="assignee.avatar"
                                      color="color"
                                      dueDate="dueDate"
                                      priority="priority"
                                      progress="progress"
                                      tags="tags"/>

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




KanbanDataSample.java

package io.jmix.uisamples.view.flowui.kanban.data;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("kanban-data")
@ViewDescriptor("kanban-data.xml")
public class KanbanDataSample extends StandardView {
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




KanbanUser.java

package io.jmix.uisamples.entity;

import io.jmix.core.FileRef;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.jspecify.annotations.Nullable;

import java.util.UUID;

@Table(name = "KANBAN_USER")
@Entity
@JmixEntity
public class KanbanUser {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @InstanceName
    @Column(name = "NAME", length = 50, nullable = false)
    private String name;

    @Column(name = "AVATAR", length = 1024)
    private FileRef avatar;

    public UUID getId() {
        return id;
    }

    public void setId(final UUID id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Nullable
    public FileRef getAvatar() {
        return avatar;
    }

    public void setAvatar(FileRef avatar) {
        this.avatar = avatar;
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




TaskPriority.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum TaskPriority implements EnumClass<String> {

    LOW("low"),
    AVERAGE("average"),
    HIGH("high"),
    CRITICAL("critical");

    private final String id;

    TaskPriority(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    @Nullable
    public static TaskPriority fromId(String id) {
        for (TaskPriority at : TaskPriority.values()) {
            if (at.getId().equals(id)) {
                return at;
            }
        }
        return null;
    }
}


