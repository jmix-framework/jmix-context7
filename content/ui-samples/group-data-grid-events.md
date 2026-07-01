<Path>Add-ons > GroupDataGrid > GroupDataGrid events</Path>

GroupDataGrid has the following specific events: GroupDataGridGroupingChangedEvent - fired when grouping is changed. CollapseEvent - fired when a group is collapsed. ExpandEvent - fired when a group is expanded. GroupDataGridGroupItemClickEvent - fired when a group row is clicked. GroupDataGridGroupItemDoubleClickEvent - fired when a group row is double-clicked.

group-data-grid-events.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:groupg="http://jmix.io/schema/groupgrid/ui">
    <data>
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_base">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <groupg:groupDataGrid id="customersGroupDataGrid"
                              dataContainer="customersDc"
                              width="100%"
                              minHeight="20em">
            <groupg:groupBy>
                <groupg:columnRef key="grade"/>
            </groupg:groupBy>
            <groupg:columns>
                <groupg:groupColumn header="msg://customersGroupDataGrid.group.header" resizable="true"/>
                <groupg:column property="grade"/>
                <groupg:column property="name"/>
                <groupg:column property="lastName"/>
                <groupg:column property="email"/>
                <groupg:column property="age"/>
                <groupg:column property="active"/>
            </groupg:columns>
        </groupg:groupDataGrid>
    </layout>
</view>




GroupDataGridEventsSample.java

package io.jmix.uisamples.view.flowui.groupdatagrid.events;

import com.google.common.base.Joiner;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.groupgrid.GroupListDataComponent;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.groupgridflowui.component.event.GroupItemClickEvent;
import io.jmix.groupgridflowui.component.event.GroupingChangedEvent;
import io.jmix.groupgridflowui.kit.vaadin.grid.Grid;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("group-data-grid-events")
@ViewDescriptor(value = "group-data-grid-events.xml")
public class GroupDataGridEventsSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("customersGroupDataGrid")
    private void onGroupingChanged(GroupingChangedEvent<Customer> event) {
        List<String> keys = event.getGroupingColumns().stream().map(Grid.Column::getKey).toList();

        notifications.create("Current grouping: %s".formatted(
                        keys.isEmpty() ? "no groups" : Joiner.on(", ").join(keys)))
                .withPosition(Notification.Position.MIDDLE)
                .show();
    }

    @Subscribe("customersGroupDataGrid")
    private void onCollapse(GroupListDataComponent.CollapseEvent<Customer> event) {
        List<String> properties = event.getCollapsedGroups().stream().map(Object::toString).toList();

        notifications.create("Collapsed groups: " + Joiner.on(", ").join(properties))
                .withPosition(Notification.Position.MIDDLE)
                .show();
    }

    @Subscribe("customersGroupDataGrid")
    private void onExpand(GroupListDataComponent.ExpandEvent<Customer> event) {
        List<String> properties = event.getExpandedGroups().stream().map(Object::toString).toList();

        notifications.create("Expanded groups: " + Joiner.on(", ").join(properties))
                .withPosition(Notification.Position.MIDDLE)
                .show();
    }

    @Subscribe("customersGroupDataGrid")
    private void onGroupItemClick(GroupItemClickEvent<Customer> event) {
        notifications.create("Clicked group: " + event.getGroupInfo())
                .withPosition(Notification.Position.MIDDLE)
                .show();
    }
}




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.jspecify.annotations.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum CustomerGrade implements EnumClass<Integer> {

    PREMIUM(10),
    HIGH(20),
    STANDARD(30);

    private final Integer id;

    CustomerGrade(Integer id) {
        this.id = id;
    }

    @Override
    public Integer getId() {
        return id;
    }

    @Nullable
    public static CustomerGrade fromId(Integer id) {
        for (CustomerGrade grade : CustomerGrade.values()) {
            if (grade.getId().equals(id))
                return grade;
        }
        return null;
    }
}


