<Path>Components > ValuePicker > Data-aware ValuePicker</Path>

The dataContainer and property attributes are used to connect the valuePicker to an entity attribute. The dataContainer contains an entity instance; property specifies an attribute to edit.

value-picker-dataaware.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <instance id="customerDc"
                  class="io.jmix.uisamples.entity.Customer"
                  fetchPlan="_local"/>
    </data>
    <layout>
        <valuePicker id="valuePicker" dataContainer="customerDc" property="name" allowCustomValue="true"
                     label="Name" helperText="Generate or type a customer name">
            <actions>
                <action id="generate" icon="REFRESH" description="Generate name"/>
                <action id="value_clear" type="value_clear"/>
            </actions>
        </valuePicker>
        <hbox>
            <span text="Value in the container:"/>
            <span id="spanValue"/>
        </hbox>
    </layout>
</view>




ValuePickerDataawareSample.java

package io.jmix.uisamples.view.flowui.components.valuepicker.dataaware;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.html.Span;
import io.jmix.core.Metadata;
import io.jmix.flowui.component.valuepicker.JmixValuePicker;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.kit.component.valuepicker.CustomValueSetEvent;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Customer;
import org.apache.commons.lang3.RandomUtils;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("value-picker-dataaware")
@ViewDescriptor("value-picker-dataaware.xml")
public class ValuePickerDataawareSample extends StandardView {

    @ViewComponent
    protected InstanceContainer<Customer> customerDc;
    @ViewComponent
    protected Span spanValue;

    @Autowired
    protected Metadata metadata;

    protected List<String> names = List.of("Katherine", "John", "Andy", "Edward", "George",
            "Philipp", "Dora", "James", "Daniel", "Michael", "Claire", "Joan", "Peter", "Martin");

    @Subscribe
    protected void onInit(InitEvent event) {
        Customer customer = metadata.create(Customer.class);
        customer.setName(getRandomName());
        customerDc.setItem(customer);
    }

    @Subscribe("valuePicker")
    protected void onValuePickerValueChange(ComponentValueChangeEvent<JmixValuePicker<String>, String> event) {
        spanValue.setText(customerDc.getItem().getName());
    }

    @Subscribe("valuePicker.generate")
    protected void onValuePickerGenerateActionPerformed(ActionPerformedEvent event) {
        customerDc.getItem().setName(getRandomName());
    }

    @Subscribe("valuePicker")
    protected void onValuePickerCustomValueChange(CustomValueSetEvent<JmixValuePicker<String>, String> event) {
        customerDc.getItem().setName(event.getText());
    }

    protected String getRandomName() {
        return names.get(RandomUtils.secure().randomInt() % names.size());
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


