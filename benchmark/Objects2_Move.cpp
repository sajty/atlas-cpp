#include <iostream>
#include <cassert>
#include "../src/Message/Object.h"
#include "../src/Objects/Root.h"
#include "../src/Objects/Operation/Operation.h"
#include "../src/Objects/Entity/Entity.h"

#include "timer.h"

using namespace Atlas;
using namespace Atlas::Objects;
using namespace Atlas::Message;
using namespace std;

#define DEBUG 0
#if DEBUG
#define MAX_ITER 10.0
#else
#define MAX_ITER 100000.0
#endif

//Plain creating of sight operation: iterations=100000 CPU Time=4.42 iter/s=22624.4
//Plain creating of sight operation: iterations=1e+07 CPU Time=1.9 iter/s=5.26316e+06

class NPC
{
public:
  NPC() : id("123") {x=y=z = vx=vy=vz = 0.0;}
  Operation::SightInstance move(Operation::MoveInstance &op);
  string getId() {return id;}
private:
  string id;
  double x,y,z;
  double vx,vy,vz;
};

Operation::SightInstance NPC::move(Operation::MoveInstance &op)
{
    Object::ListType::const_iterator new_vel_i =
        ((Entity::GameEntityInstance&)op->getArgs()[0])->
        getVelocity().begin();
    vx = (*new_vel_i).AsFloat();
    new_vel_i++; vy = (*new_vel_i).AsFloat();
    new_vel_i++; vz = (*new_vel_i).AsFloat();
    
    x += vx;
    y += vy;
    z += vz;
    
    //human:
    Entity::GameEntityInstance human;
    //Entity::GameEntity human = Entity::GameEntity::Instantiate();
    human->setId(getId());
    Object::ListType pos;
    pos.push_back(x);
    pos.push_back(y);
    pos.push_back(z);
    human->setPos(pos);
    Object::ListType vel;
    vel.push_back(vx);
    vel.push_back(vy);
    vel.push_back(vz);
    human->setVelocity(vel);
    
    //move:
    Operation::MoveInstance move;
    //Operation::Move move = Operation::Move::Instantiate();
    vector<Root> move_args(1);
    move_args[0] = (Root&)human;
    move->setArgs(move_args);

    //sight:
    Operation::SightInstance sight;
    //Operation::Sight sight = Operation::Sight::Instantiate();
    sight->setFrom(getId());
    vector<Root> sight_args(1);
    sight_args[0] = (Root&)move;
    sight->setArgs(sight_args);
    
    return sight;
}

int main(int argc, char** argv)
{
    double i;
    TIME_ON;
    for(i=0; i<MAX_ITER; i+=1.0) {
        //human:
        Entity::GameEntityInstance human;
        Object::ListType pos;
        pos.push_back(i);
        pos.push_back(i-1.0);
        pos.push_back(i+1.0);
        human->setPos(pos);
        
        Object::ListType vel;
        vel.push_back(i);
        vel.push_back(i-1.0);
        vel.push_back(i+1.0);
        human->setVelocity(vel);
//        Object::ListType foo = human->getVelocity();
//        cout<<foo.size()<<":"<<foo.front().asFloat()<<","<<foo.back().asFloat()<<endl;

        //move:
        Operation::MoveInstance move;
        vector<Root> move_args(1);
        move_args[0] = (Root&)human;
        move->setArgs(move_args);
//        Object::MapType ent = move.getArgs().front().asMap();
//        cout<<"vel0:"<<ent["velocity"].asList().front().asFloat()<<endl;

        //sight:
        Operation::SightInstance sight;
        sight->setFrom("123");
        vector<Root> sight_args(1);
        sight_args[0] = (Root&)move;
        sight->setArgs(sight_args);
//        Object::MapType ent = sight.getArgs().front().asMap()
//          ["args"].asList().front().asMap();
//        cout<<"vel0:"<<ent["velocity"].asList().front().asFloat()<<endl;
    }
    TIME_OFF("Plain creating of sight operation");
    NPC npc1;
    double x,y,z;
    TIME_ON;
    for(i=0; i<MAX_ITER; i+=1.0) {
        //human:
        Entity::GameEntityInstance human;
        human->setId(npc1.getId());
        Object::ListType vel;
        vel.push_back(i);
        vel.push_back(i-1.0);
        vel.push_back(i+1.0);
        human->setVelocity(vel);
        
        //move:
        Operation::MoveInstance move;
        vector<Root> move_args(1);
        move_args[0] = (Root&)human;
        move->setArgs(move_args);

        Operation::SightInstance res_sight = npc1.move(move);
        Object::ListType::const_iterator new_pos_i =
            ((Entity::GameEntityInstance&)
               ((Operation::MoveInstance&)res_sight->getArgs()[0])
             ->getArgs()[0])->
            getVelocity().begin();
        x = (*new_pos_i).asFloat();
        new_pos_i++; y = (*new_pos_i).asFloat();
        new_pos_i++; z = (*new_pos_i).asFloat();
    }
    TIME_OFF("NPC movements");
    cout<<"Resulting position: ("<<x<<","<<y<<","<<z<<")"<<endl;
    return 0;
}