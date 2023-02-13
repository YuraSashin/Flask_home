public class Characters {
    protected String name;
    protected int hp;
    protected int attack;
    protected int speed;

    public Characters(String name, int hp, int attack, int speed){
        this.name = name;
        this.hp = hp;
        this.attack = attack;
        this.speed = speed;
    }

    public int getAttack(){
        return 0;
    }

    public int getHp() {
        return 0;
    }

    public int getSpeed(){
        return 0;
    }
} 

