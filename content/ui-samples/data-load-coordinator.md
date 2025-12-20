<Path>Facets > DataLoadCoordinator</Path>

dataLoadCoordinator facet is designed for triggering data loaders and for declarative linking of data loaders to data containers, visual components, and view lifecycle events. There are three working modes: Automatic mode is activated by auto attribute. A loaders are triggered on BeforeShowEvent. Manual mode uses nested refresh elements that control when the data loaders must be triggered. Semi-automatic mode is a combination of automatic and manual modes. When the auto attribute is set to true, and there are some manually configured triggers, DataLoadCoordinator will automatically configure all loaders having no manual configuration.

data-load-coordinator.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
        <collection id="ordersDc"
                    class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_local">
                <property name="customer" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="ordersDl">
                <query>
                    <![CDATA[select e from uisamples_Order e order by e.date]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator>
            <refresh loader="ordersDl">
                <onViewEvent type="Ready"/>
            </refresh>
        </dataLoadCoordinator>
    </facets>
    <layout>
        <h4 text="CollectionContainer items count:"/>
        <div classNames="flex flex-row flex-wrap gap-s">
            <icon icon="HAMMER"/>
            <span text="onInit:"/>
            <span id="onInitItemCount"/>
        </div>
        <div classNames="flex flex-row flex-wrap gap-s">
            <icon icon="BROWSER"/>
            <span text="onBeforeShow:"/>
            <span id="onBeforeShowItemCount"/>
        </div>
        <div classNames="flex flex-row flex-wrap gap-s">
            <icon icon="CHECK"/>
            <span text="onReady:"/>
            <span id="onReadyItemCount"/>
        </div>
        <dataGrid id="dataGrid" width="100%" minHeight="20em"
                  dataContainer="ordersDc">
            <columns>
                <column property="date"/>
                <column property="customer"/>
                <column property="amount"/>
                <column property="description"/>
            </columns>
        </dataGrid>
    </layout>
</view>




DataLoadCoordinatorSample.java

package io.jmix.uisamples.view.flowui.facets.dataloadcoordinator;

import com.vaadin.flow.component.html.Span;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Order;

@ViewController("data-load-coordinator")
@ViewDescriptor("data-load-coordinator.xml")
public class DataLoadCoordinatorSample extends StandardView {

    @ViewComponent
    protected CollectionContainer<Order> ordersDc;

    @ViewComponent
    protected Span onInitItemCount;
    @ViewComponent
    protected Span onBeforeShowItemCount;
    @ViewComponent
    protected Span onReadyItemCount;

    @Subscribe
    public void onInit(InitEvent event) {
        onInitItemCount.setText(String.valueOf(ordersDc.getItems().size()));
    }

    @Subscribe
    public void onBeforeShow(BeforeShowEvent event) {
        onBeforeShowItemCount.setText(String.valueOf(ordersDc.getItems().size()));
    }

    @Subscribe
    public void onReady(ReadyEvent event) {
        onReadyItemCount.setText(String.valueOf(ordersDc.getItems().size()));
    }
}




Order.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.UUID;

@Table(name = "ORDER")
@Entity(name = "uisamples_Order")
@JmixEntity
public class Order {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "CUSTOMER_ID")
    private Customer customer;

    @Temporal(TemporalType.DATE)
    @Column(name = "DATE_", nullable = false)
    @InstanceName
    private Date date;

    @Column(name = "AMOUNT")
    private BigDecimal amount;

    @Column(name = "DESCRIPTION")
    private String description;

    @OrderBy("rowNum")
    @Composition
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setItems(List<OrderItem> items) {
        this.items = items;
    }

    public List<OrderItem> getItems() {
        return items;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public Date getDate() {
        return date;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    public BigDecimal getAmount() {
        return amount;
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
import org.springframework.lang.Nullable;

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


