<Path>Add-ons > Kanban > Kanban data saving</Path>

There are two ways to save changes for the Kanban board component: manual (default) and automatic. Using the component, it is possible to change three attributes of the entity: status, swimlane - by dragging Kanban task cards into different columns priority - using the corresponding drop-down list next to the text on the Kanban task card Changes are automatically commited in the data container, but by default do not initiate saving to the database. In manual mode, you must define SaveDelegate, which will be called each time you change cards using the Kanban board. In automatic mode, you must set the attribute autoSave in XML to true. This will automatically set the SaveDelegate in the component, which will save the DataContext of the current view. Be careful, the entire view data context will be saved.

kanban-data-saving.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:kanban="http://jmix.io/schema/kanban/ui">
    <data readOnly="true">
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
        <tabSheet id="tabSheet" width="100%" height="100%">
            <tab id="saveDelegateTab" label="msg://saveDelegateTab.label">
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

                    <kanban:columns>
                        <kanban:column dataField="todo" label="msg://kanban.column.todo"/>
                        <kanban:column dataField="in_progress" label="msg://kanban.column.in_progress"/>
                        <kanban:column dataField="testing" label="msg://kanban.column.testing"/>
                        <kanban:column dataField="done" label="msg://kanban.column.done"/>
                    </kanban:columns>
                </kanban:kanban>
            </tab>
            <tab id="autoSaveTab" label="msg://autoSaveTab.label">
                <kanban:kanban dataContainer="kanbanTasksDc" autoSave="true"
                               width="100%"
                               height="100%"
                               taskDueDateVisible="true"
                               taskPriorityVisible="true"
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

                    <kanban:columns>
                        <kanban:column dataField="todo" label="msg://kanban.column.todo"/>
                        <kanban:column dataField="in_progress" label="msg://kanban.column.in_progress"/>
                        <kanban:column dataField="testing" label="msg://kanban.column.testing"/>
                        <kanban:column dataField="done" label="msg://kanban.column.done"/>
                    </kanban:columns>
                </kanban:kanban>
            </tab>
        </tabSheet>
    </layout>
</view>




KanbanDataSavingSample.java

package io.jmix.uisamples.view.flowui.kanban.datasaving;

import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.KanbanTask;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("kanban-data-saving")
@ViewDescriptor("kanban-data-saving.xml")
public class KanbanDataSavingSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Install(to = "kanban", subject = "saveDelegate")
    public void kanbanSaveDelegate(final KanbanTask kanbanTask) {
        notifications.create("Task '%s' saved!".formatted(kanbanTask.getName()))
                .withThemeVariant(NotificationVariant.SUCCESS)
                .withPosition(Notification.Position.TOP_END)
                .show();
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


