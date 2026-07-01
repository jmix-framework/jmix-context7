<Path>Components > EntityPicker > EntityPicker with MetaClass</Path>

EntityPicker can be used without any direct reference to data, i.e., without dataContainer and property attributes. In this case metaClass attribute should be used to specify an entity type for EntityPicker. In this example, the component works with Customer entity which has Customer metadata class name.

entity-picker-meta-class.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <entityPicker id="entityPicker" metaClass="Customer"
                      placeholder="Choose a customer"
                      width="15em">
            <actions>
                <action id="lookup" type="entity_lookup"/>
                <action id="clear" type="entity_clear"/>
            </actions>
        </entityPicker>
    </layout>
</view>




EntityPickerMetaClassSample.java

package io.jmix.uisamples.view.flowui.components.entitypicker.metaclass;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.core.MetadataTools;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.valuepicker.EntityPicker;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("entity-picker-meta-class")
@ViewDescriptor("entity-picker-meta-class.xml")
public class EntityPickerMetaClassSample extends StandardView {

    @Autowired
    protected MetadataTools metadataTools;
    @Autowired
    protected Notifications notifications;

    @Subscribe("entityPicker")
    protected void onEntityPickerValueChange(ComponentValueChangeEvent<EntityPicker<Customer>, Customer> event) {
        String str = event.getValue() == null
                ? "null"
                : metadataTools.getInstanceName(event.getValue());
        notifications.show("value = " + str);
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


