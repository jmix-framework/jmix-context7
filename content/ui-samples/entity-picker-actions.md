<Path>Components > EntityPicker > EntityPicker actions</Path>

For EntityPicker, you can define an arbitrary number of actions, displayed as buttons on the right. It can be done either in the XML descriptor using the actions nested element, or programmatically in the controller using addAction(). In this example, we have defined three actions in XML: standard entity_lookup and entity_open, and custom greeting. In the controller, we have added showGrade custom action and entity_clear standard action with the redefined icon.

entity-picker-actions.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="orderDc"
                  class="io.jmix.uisamples.entity.Order">
            <fetchPlan extends="_local">
                <property name="customer" fetchPlan="_local"/>
            </fetchPlan>
        </instance>
    </data>
    <layout>
        <entityPicker id="entityPicker"
                      dataContainer="orderDc"
                      property="customer"
                      placeholder="Choose a customer"
                      width="20em">
            <actions>
                <action id="lookup" type="entity_lookup"/>
                <action id="open" type="entity_open"/>
                <action id="greeting" icon="MAGIC"/>
            </actions>
        </entityPicker>
    </layout>
</view>




EntityPickerActionsSample.java

package io.jmix.uisamples.view.flowui.components.entitypicker.actions;

import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.core.Metadata;
import io.jmix.flowui.Actions;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.action.entitypicker.EntityClearAction;
import io.jmix.flowui.component.valuepicker.EntityPicker;
import io.jmix.flowui.kit.action.Action;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.kit.action.BaseAction;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.Order;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("entity-picker-actions")
@ViewDescriptor("entity-picker-actions.xml")
public class EntityPickerActionsSample extends StandardView {

    @ViewComponent
    protected EntityPicker<Customer> entityPicker;
    @ViewComponent
    protected InstanceContainer<Order> orderDc;

    @Autowired
    protected Metadata metadata;
    @Autowired
    protected Notifications notifications;
    @Autowired
    protected Actions actions;

    @Subscribe
    protected void onInit(InitEvent event) {
        initDc();
        initEntityPickerActions();
    }

    protected void initDc() {
        // InstanceContainer initialization. It is usually done automatically if the view is
        // inherited from StandardDetailView and is used as an entity detail.
        Order order = metadata.create(Order.class);
        orderDc.setItem(order);
    }

    protected void initEntityPickerActions() {
        entityPicker.addAction(createShowGradeAction());
        entityPicker.addAction(createEntityClearAction());
    }

    @Subscribe("entityPicker.greeting")
    protected void onEntityPickerGreetingActionPerformed(ActionPerformedEvent event) {
        Customer customer = entityPicker.getValue();

        if (customer != null) {
            notifications.show("Hello, " + customer.getName());
        } else {
            notifications.show("Choose a customer");
        }
    }

    protected Action createShowGradeAction() {
        return new BaseAction("showGrade")
                .withIcon(VaadinIcon.ACADEMY_CAP.create())
                .withHandler(actionPerformedEvent -> {
                    Customer customer = entityPicker.getValue();

                    if (customer != null) {
                        notifications.show(customer.getName() + "'s grade is " + customer.getGrade());
                    } else {
                        notifications.show("Choose a customer");
                    }
                });
    }

    protected Action createEntityClearAction() {
        Action entityClearAction = actions.create(EntityClearAction.ID);
        entityClearAction.setIcon(VaadinIcon.BAN.create());

        return entityClearAction;
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


